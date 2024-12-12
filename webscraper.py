from colorama import init, Fore, Style
import random
import os
import requests
from datetime import datetime
import time
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor
import asyncio
import re
from instances import info, success, error, newlog, newlog1
from spammer import spam_messages

init(autoreset=True)

current_time = datetime.now().strftime("%H:%M:%S")

test = "tes2t"
os.system("cls")

main_webhook = open("webhook_log.txt").read().strip()

def check_webhook():
    current_time = datetime.now().strftime("%H:%M:%S")
    if main_webhook == "YOUR_WEBHOOK_HERE":
        error(f"No webhook provided in webhook_log.txt!")
        error(f"Submissions cannot be logged without a webhook")
        exit(1)
    else:
        webhook_req = requests.get(main_webhook)
        if webhook_req.status_code == 200:
            success(f"[{Fore.CYAN}{current_time}{Style.RESET_ALL}] {Fore.GREEN}Valid webhook {Fore.WHITE}[{Fore.GREEN}200{Fore.WHITE}]{Style.RESET_ALL} 🎄")
        else:
            error(f"[{Fore.CYAN}{current_time}{Style.RESET_ALL}] {Fore.RED}Invalid webhook {Fore.WHITE}[{Fore.RED}404{Fore.WHITE}]{Style.RESET_ALL} 🎄")
            exit(1)
check_webhook()

triage_url = "https://tria.ge/s?q=score:10 AND tag:pyinstaller or family:blankgrabber or family:discordrat or family:pysilon&limit=1"
processed_ids = set()
triage_api_key = open("api_key.txt").read().strip().replace("Bearer", "")
triage_get_request = requests.get(f'https://tria.ge/api/v0/samples/241105-q57r2ashqn/sample', headers={"Authorization": f"Bearer {triage_api_key}"})
if triage_get_request.status_code != 200:
    print(f"[{Fore.CYAN}{current_time}{Style.RESET_ALL}] {Fore.RED}Invalid API Key in api_key.txt{Style.RESET_ALL} 🎄")
    time.sleep(0.5)
    print(f"[{Fore.CYAN}{current_time}{Style.RESET_ALL}] {Fore.RED}Decompiling feature unavailable{Style.RESET_ALL} ❄️")
    time.sleep(3)
else:
    success(f"[{Fore.CYAN}{current_time}{Style.RESET_ALL}] {Fore.GREEN}API Connected!{Style.RESET_ALL} 🎅")
    time.sleep(0.5)
    success(f"[{Fore.CYAN}{current_time}{Style.RESET_ALL}] {Fore.GREEN}Decompiler Ready{Style.RESET_ALL} ❄️")
    time.sleep(3)

now = datetime.now()
current_time = now.strftime("%H:%M:%S")

async def process_submission(report_id, file_name, fams, score, time_uploaded, tags):
    current_time = datetime.now().strftime("%H:%M:%S")
    if fams in ['asyncrat', 'atomsilo', 'blackmatter', 'cerber', 'urelas', 'xmrig', 'metasploit', 'xworm', 'cryptbot', 'cyrat', 'acobaltstrike', 'umbral', 'blacknet', 'berbew', 'blackmoon', 'emotet', 'mydoom', 'neshta', 'doomrat', 'shadowrat']:
        error(f"Blacklisted: {fams}")
        error(f"File: {file_name}")
        os.system("cls")
        return

    if file_name.endswith((".zip", ".rar", ".7z", ".tar", ".sh", ".bat")):
        info("This extension is not supported. Skipping file")
        time.sleep(3)
        os.system("cls")
        return

    try:
        info("Decompiling...")
        file_content = requests.get(f'https://tria.ge/api/v0/samples/{report_id}/sample', headers={"Authorization": f"Bearer {triage_api_key}"}).content

        ilikeblack = requests.post('https://lululepu.fr/ungrabber', files={'file': file_content})
        response2 = ilikeblack.json()

        def contains_base64(text):
            base64_regex = r'(?:[A-Za-z0-9+/]{4})*(?:[A-Za-z0-9+/]{2}==|[A-Za-z0-9+/]{3}=)?'
            return re.search(base64_regex, text) is not None

        if response2 and 'result' in response2:
            result = response2['result']
            if "webhook" in result:
                success(f"[{Fore.CYAN}{current_time}{Style.RESET_ALL}] {Fore.GREEN}Webhook valid!{Style.RESET_ALL} 🎄")
                os.system("cls")
                spam_messages(result, 2)
                requests.post(main_webhook, data={"content": f"🎅 **New Valid Webhook** 🎄\n`{result}` ❄️ @everyone"})
            elif contains_base64(result):
                success("🎅 Successfully decompiled Base64 string: 🎄 " + result)
                requests.post(main_webhook, data={"content": f"🎅 **New Token** 🎄\n`{result}` ❄️ @everyone"})

    except Exception as e:
        print(f"[{Fore.CYAN}{current_time}{Style.RESET_ALL}] {Fore.RED}Error fetching or processing file: {e}{Style.RESET_ALL} 🎄")

def check_for_new_submissions():
    global processed_ids

    response = requests.get(triage_url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        report_items = soup.find_all('a', class_='row alert')
        with ThreadPoolExecutor(max_workers=10) as executor:
            for report in report_items:
                report_id = report['data-sample-id']
                if report_id in processed_ids:
                    continue

                file_name = "Unknown file"
                score = None
                tags = []

                file_name_div = report.find('div', class_='column-target')
                if file_name_div:
                    file_name = file_name_div.text.strip()

                score_div = report.find('div', class_='column-score')
                if score_div:
                    score_text = score_div.find('div', class_='score').text
                    score = float(score_text.strip()) if score_text else None

                tags_div = report.find('div', class_='column-tags')
                if tags_div:
                    tags = [tag.text.strip() for tag in tags_div.find_all('span')]

                time_uploaded = report.find('div', class_="column-created").text.replace('UTC', '\n').strip()

                fams_element = report.find('span', class_="rose")
                fams = fams_element.text if fams_element else "No family"

                os.system("cls")

                if score is not None and score > 6:
                    log_entries = [
                        ("🎄 ID:", report_id),
                        ("🎅 Name:", file_name),
                        ("⭐ Score:", score),
                        ("🎁 Family:", fams),
                        ("❄️  Tags:", ', '.join(tags) if tags else 'No tags'),
                        ("🔔 Time Uploaded:", time_uploaded)
                    ]

                    print("\n" + "─" * 50 + "\n")
                    for title, value in log_entries:
                        newlog1(f"{title} {value}")
                    print("\n" + "─" * 50 + "\n")

                    random_color = random.choice([0xFF0000, 0x00FF00, 0xFFD700, 0x0000FF, 0xFF00FF, 0x00FFFF, 0x800080, 0xFFA500, 0x008000, 0x800000])

                    logEmbed = {
                        "title": f"🎄 {report_id}",
                        "fields": [
                            {"name": "🎅 Name", "value": file_name},
                            {"name": "🎄 Tags", "value": ', '.join(tags) if tags else 'No tags'},
                            {"name": "🎅 Time Uploaded", "value": time_uploaded},
                            {"name": "🎄 Family", "value": fams}
                        ],
                        "color": random_color,
                        "footer": {"text": "🎅 Monokai was here 🎄"}
                    }
                    try:
                        requests.post(main_webhook, json={"embeds": [logEmbed]})
                    except Exception as e:
                        print(e)

                executor.submit(lambda: asyncio.run(process_submission(report_id, file_name, fams, score, time_uploaded, tags)))

                processed_ids.add(report_id)

                if 'discordrat' in tags:
                    success(f"[{Fore.CYAN}{current_time}{Style.RESET_ALL}] {Fore.GREEN}Found DiscordRAT in submission{Style.RESET_ALL} 🎅 https://tria.ge/{report_id}")
                    requests.post(main_webhook, data={"content": f"🎄 **DiscordRAT** 🎅\nDiscordRAT Found in Submission {report_id}! ❄️ @everyone"})

def main():
    while True:
        check_for_new_submissions()
        info("Scanning for New Submissions... ❄️ ")
        time.sleep(0.5)

if __name__ == "__main__":
    main()
