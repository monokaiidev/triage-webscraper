from colorama import init, Fore, Style
import random
import os
import requests
from datetime import datetime, UTC
import time, webbrowser
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor
import asyncio
import re
from spammer import spam_messages

init(autoreset=True)

current_time = datetime.now().strftime("%H:%M:%S")

test = "tes2t"
os.system("cls")
print(f"[{Fore.CYAN}{current_time}{Style.RESET_ALL}] {Fore.GREEN}Welcome to the Triage Webscraper! {Fore.WHITE}[{Fore.GREEN}200{Fore.WHITE}]{Style.RESET_ALL} 🎄")
time.sleep(2)
webbrowser.open("https://github.com/monokaiidev")


main_webhook = open("webhook_log.txt").read().strip()

def check_webhook():
    current_time = datetime.now().strftime("%H:%M:%S")
    if main_webhook == "YOUR_WEBHOOK_HERE":
        print(f"[{Fore.CYAN}{current_time}{Style.RESET_ALL}] {Fore.RED}No webhook specified! {Fore.WHITE}[{Fore.RED}404{Fore.WHITE}]{Style.RESET_ALL} 🎄")
        exit(1)
    else:
        webhook_req = requests.get(main_webhook)
        if webhook_req.status_code == 200:
            print(f"[{Fore.CYAN}{current_time}{Style.RESET_ALL}] {Fore.GREEN}Valid webhook {Fore.WHITE}[{Fore.GREEN}200{Fore.WHITE}]{Style.RESET_ALL} 🎄")
        else:
            print(f"[{Fore.CYAN}{current_time}{Style.RESET_ALL}] {Fore.RED}Invalid webhook {Fore.WHITE}[{Fore.RED}404{Fore.WHITE}]{Style.RESET_ALL} 🎄")
            exit(1)
check_webhook()

triage_url = "https://tria.ge/s?q=score:10 AND tag:pyinstaller or family:blankgrabber or family:discordrat or family:pysilon&limit=1"
processed_ids = set()
triage_api_key = open("api_key.txt").read().strip().replace("Bearer", "")
triage_get_request = requests.get(f'https://tria.ge/api/v0/samples/241105-q57r2ashqn/sample', headers={"Authorization": f"Bearer {triage_api_key}"})
if triage_get_request.status_code != 200:
    print(f"[{Fore.CYAN}{current_time}{Style.RESET_ALL}] {Fore.GREEN}Connecting to API... {Fore.WHITE}[{Fore.GREEN}200{Fore.WHITE}]{Style.RESET_ALL} 🎄")
    time.sleep(3)
    print(f"[{Fore.CYAN}{current_time}{Style.RESET_ALL}] {Fore.GREEN}Trying to connect to API... {Fore.WHITE}[{Fore.RED}500{Fore.WHITE}]{Style.RESET_ALL} 🎄")
    time.sleep(3)
    print(f"[{Fore.CYAN}{current_time}{Style.RESET_ALL}] {Fore.RED}Invalid API Key in api_key.txt{Style.RESET_ALL} 🎄")
    time.sleep(0.5)
    print(f"[{Fore.CYAN}{current_time}{Style.RESET_ALL}] {Fore.RED}Decompiling feature unavailable{Style.RESET_ALL} ❄️")
    time.sleep(3)
else:
    print(f"[{Fore.CYAN}{current_time}{Style.RESET_ALL}] {Fore.GREEN}Connecting to API... {Fore.WHITE}[{Fore.GREEN}200{Fore.WHITE}]{Style.RESET_ALL} 🎄")
    time.sleep(3)
    print(f"[{Fore.CYAN}{current_time}{Style.RESET_ALL}] {Fore.GREEN}API Connected!{Style.RESET_ALL} 🎅")
    time.sleep(0.5)
    print(f"[{Fore.CYAN}{current_time}{Style.RESET_ALL}] {Fore.GREEN}Decompiler Ready{Style.RESET_ALL} ❄️")
    time.sleep(3)

current_time = datetime.now().strftime("%H:%M:%S")

def decompile_file(file_content):
    current_time = datetime.now().strftime("%H:%M:%S")
    try:
        if triage_get_request.status_code != 200:
            print(f"[{Fore.CYAN}{current_time}{Style.RESET_ALL}] {Fore.RED}Cannot decompile: Invalid or missing API key{Style.RESET_ALL} 🎄")
            return None

        ilikeblack = requests.post('https://lululepu.fr/ungrabber', files={'file': file_content})
        response2 = ilikeblack.json()

        if response2 and 'result' in response2:
            return response2['result']
        return None
    except Exception as e:
        print(f"[{Fore.CYAN}{current_time}{Style.RESET_ALL}] {Fore.RED}Decompiling error: {e}{Style.RESET_ALL} 🎄")
        return None

async def process_submission(report_id, file_name, fams, score, time_uploaded, tags):
    current_time = datetime.now().strftime("%H:%M:%S")
    if fams in ['asyncrat', 'atomsilo', 'blackmatter', 'cerber', 'urelas', 'xmrig', 'metasploit', 'xworm', 'cryptbot', 'cyrat', 'acobaltstrike', 'umbral', 'blacknet', 'berbew', 'blackmoon', 'emotet', 'mydoom', 'neshta', 'doomrat', 'shadowrat']:
        print(f"[{Fore.CYAN}{current_time}{Style.RESET_ALL}] {Fore.RED}Blacklisted: {fams}{Style.RESET_ALL}")
        print(f"[{Fore.CYAN}{current_time}{Style.RESET_ALL}] {Fore.RED}File: {file_name}{Style.RESET_ALL}")
        os.system("cls")
        return

    if file_name.endswith((".zip", ".rar", ".7z", ".tar", ".sh", ".bat")):
        print(f"[{Fore.CYAN}{current_time}{Style.RESET_ALL}] {Fore.WHITE}This extension is not supported. Skipping file{Style.RESET_ALL}")
        time.sleep(3)
        os.system("cls")
        return

    try:
        print(f"[{Fore.CYAN}{current_time}{Style.RESET_ALL}] {Fore.WHITE}Decompiling...{Style.RESET_ALL}")
        file_content = requests.get(f'https://tria.ge/api/v0/samples/{report_id}/sample', headers={"Authorization": f"Bearer {triage_api_key}"}).content

        def contains_base64(result):
            import re
            base64_pattern = r'^[A-Za-z0-9+/]*={0,2}$'
            return bool(re.match(base64_pattern, result))

        result = decompile_file(file_content)
        if result:
            if "webhook" in result:
                webhook_test = requests.get(result)
                if webhook_test.status_code == 200:
                    print(f"[{Fore.CYAN}{current_time}{Style.RESET_ALL}] {Fore.WHITE}Valid webhook! {Fore.RED}{result}{Style.RESET_ALL} 🎄")
                    os.system("cls")
                    spam_messages(result, 2)
                    requests.post(main_webhook, data={"content": f"🎅 **New Valid Webhook** 🎄\n`{result}` ❄️ @everyone"})
                    requests.post(main_webhook, data={"content": f"🎅 **New Valid Webhook** 🎄\n`{result}` ❄️ @everyone"})
                else:
                    print(f"[{Fore.CYAN}{current_time}{Style.RESET_ALL}] {Fore.WHITE}Invalid webhook: {Fore.RED}{result}{Style.RESET_ALL} 🎄")
                    requests.post(main_webhook, data={"content": f"🎅 **Invalid Webhook** 🎄\n`{result}` ❄️ @everyone"})
            elif contains_base64(result):
                print(f"[{Fore.CYAN}{current_time}{Style.RESET_ALL}] {Fore.GREEN}Successfully decompiled Base64 string: {result}{Style.RESET_ALL} 🎄")
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
                        ("🎄 ID:", f"{Fore.CYAN}{report_id}{Style.RESET_ALL}"),
                        ("🎅 Name:", f"{Fore.WHITE}{file_name}{Style.RESET_ALL}"),
                        ("⭐ Score:", f"{Fore.RED if score > 8 else Fore.WHITE}{score}{Style.RESET_ALL}"),
                        ("🎁 Family:", f"{Fore.MAGENTA}{fams}{Style.RESET_ALL}"),
                        ("❄️  Tags:", f"{Fore.BLUE}{', '.join(tags) if tags else 'No tags'}{Style.RESET_ALL}"),
                        ("🔔 Time:", f"{Fore.GREEN}{time_uploaded}{Style.RESET_ALL}")
                    ]

                    box_width = 54
                    BORDER = Fore.BLUE + Style.BRIGHT
                    TITLE = Fore.CYAN + Style.BRIGHT
                    VALUE = Fore.WHITE
                    SCORE_HIGH = Fore.RED + Style.BRIGHT
                    SCORE_MED = Fore.YELLOW + Style.BRIGHT

                    print(f"{BORDER}┌{'─' * (box_width-2)}┐{Style.RESET_ALL}")
                    for title, value in log_entries:
                        if title == "❄️ Tags:":
                            max_tag_length = 25
                            tags_str = value
                            if len(tags_str) > max_tag_length:
                                tags_str = value[:max_tag_length] + f"{Fore.CYAN}...{Style.RESET_ALL}"

                            padding = box_width - len(title) - len(tags_str) - 4
                            if padding < 0: padding = 0
                            print(f"{BORDER} {TITLE}{title}{Style.RESET_ALL} {VALUE}{tags_str}{' ' * padding} {BORDER}{Style.RESET_ALL}")
                        else:
                            padding = box_width - len(title) - len(value) - 4
                            print(f"{BORDER} {TITLE}{title}{Style.RESET_ALL} {VALUE}{value}{Style.RESET_ALL}{' ' * padding} {BORDER}{Style.RESET_ALL}")
                    print(f"{BORDER}└{'─' * (box_width-2)}┘{Style.RESET_ALL}\n")

                    random_color = random.choice([
                        0x00FFFF,
                        0x4169E1,
                        0xFF1493,
                        0x32CD32,
                        0x9370DB,
                        0x00CED1,
                    ])

                    logEmbed = {
                        "title": f"🎄 New Malware Submission Detected 🎄",
                        "description": f"**Report ID:** {report_id}",
                        "fields": [
                            {"name": "🎅 File Name", "value": f"`{file_name}`", "inline": True},
                            {"name": "⭐ Risk Score", "value": f"`{score}/10`", "inline": True},
                            {"name": "🎁 Family", "value": f"`{fams}`", "inline": True},
                            {"name": "❄️ Tags", "value": f"`{', '.join(tags) if tags else 'No tags'}`"},
                            {"name": "🔔 Upload Time", "value": f"`{time_uploaded}`", "inline": True}
                        ],
                        "color": random_color,
                        "footer": {"text": "🎅 Triage Webscraper • Made with ️"},
                        "timestamp": datetime.now(UTC).isoformat()
                    }
                    try:
                        requests.post(main_webhook, json={"embeds": [logEmbed]})
                    except Exception as e:
                        print(e)

                executor.submit(lambda: asyncio.run(process_submission(report_id, file_name, fams, score, time_uploaded, tags)))

                processed_ids.add(report_id)

                if 'discordrat' in tags:
                    print(f"[{Fore.CYAN}{current_time}{Style.RESET_ALL}] {Fore.GREEN}Found DiscordRAT in submission{Style.RESET_ALL} 🎅 https://tria.ge/{report_id}")
                    requests.post(main_webhook, data={"content": f"🎄 **DiscordRAT** 🎅\nDiscordRAT Found in Submission {report_id}! ❄️ @everyone"})

def main():
    try:
        print(f"{Fore.GREEN}{'='*20} TRIAGE WEBSCRAPER {'='*20}{Style.RESET_ALL}")
        print(f"{Fore.CYAN}Starting webscraper...{Style.RESET_ALL}")
        while True:
            check_for_new_submissions()
            print(f"[{Fore.CYAN}{current_time}{Style.RESET_ALL}] {Fore.WHITE}Scanning for new submissions...{Style.RESET_ALL}", end='\r')
            time.sleep(0.5)
    except KeyboardInterrupt:
         print(f"[{Fore.CYAN}{current_time}{Style.RESET_ALL}] {Fore.RED}Exiting...{Style.RESET_ALL}")
         exit(0)
    except Exception as e:
        print(f"[{Fore.CYAN}{current_time}{Style.RESET_ALL}] {Fore.RED}An error occured: {e}{Style.RESET_ALL}")
        exit(1)

if __name__ == "__main__":
    main()
