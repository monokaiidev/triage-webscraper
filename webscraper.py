import time
import os
import requests
from bs4 import BeautifulSoup
from colorama import init, Fore, Style
from datetime import datetime
import threading
from concurrent.futures import ThreadPoolExecutor
import asyncio
from instances import info, success, error, newlog
import re
import webbrowser

##
##
##
##
##
### PLEASE PUT YOUR API KEY IN api_key.txt. THANK YOU. DO NOT USE THIS AS YOUR PROGRAM, AS IT IS MADE BY MONOKAI
### monokai.proo ON DISCORD!
##
##
##
##
##

init(autoreset=True)

os.system("cls")

triage_url = "https://tria.ge/s?q=score:10 AND tag:pyinstaller or family:blankgrabber or family:discordrat&limit=1"
processed_ids = set()
triage_api_key = open("api_key.txt").read().strip().replace("Bearer","")
triage_get_request = requests.get(f'https://tria.ge/api/v0/samples/241105-q57r2ashqn/sample', headers={"Authorization": f"Bearer {triage_api_key}"})
if triage_get_request.status_code != 200:
    error("The API Key you typed in is invalid. Please put in a valid API Key in the file api_key.txt!")
    time.sleep(0.5)
    error("This means you will not have access to decompiling!")
    time.sleep(3)
else:
    success("Valid API Key! Continuing..")
    time.sleep(0.5)
    success("You will have access to decompiling!")
    time.sleep(3)

now = datetime.now()
current_time = now.strftime("%H:%M:%S")


async def process_submission(report_id, file_name, fams, score, time_uploaded, tags):
    if fams in ['asyncrat', 'atomsilo', 'blackmatter', 'cerber', 'urelas', 'xmrig', 'metasploit', 'xworm', 'cryptbot', 'cyrat', 'acobaltstrike', 'umbral', 'blacknet', 'berbew', 'blackmoon', 'emotet', 'mydoom', 'neshta', 'doomrat', 'shadowrat', 'redline']:
        error(f"Skipping blacklisted family with the name {Fore.RED}{file_name}{Fore.WHITE} and family {Fore.RED}{fams}{Fore.WHITE}. Not downloading file.")
        return

    if file_name.endswith((".zip", ".rar", ".7z", ".tar", ".sh", ".bat")):
        error("This extension is not supported. Not downloading file.\n")
        return
    try:
        info("Decompiling...\n")
        file_content = requests.get(f'https://tria.ge/api/v0/samples/{report_id}/sample', headers={"Authorization": f"Bearer {triage_api_key}"}).content

        ilikeblack = requests.post('https://lululepu.fr/ungrabber', files={'file': file_content})
        response2 = ilikeblack.json()

        def contains_base64(text):
            base64_regex = r'(?:[A-Za-z0-9+/]{4})*(?:[A-Za-z0-9+/]{2}==|[A-Za-z0-9+/]{3}=)?'
            return re.search(base64_regex, text) is not None


        if response2 and 'result' in response2:
            result = response2['result']
            if "webhook" in result:
                success(f"Successfully decompiled webhook: {result}")

                decomp = requests.get(result)
                if decomp.status_code == 200:
                    success("Webhook valid!")
                    time.sleep(5)
                    os.system("cls")
                else:
                    error("404")
                    time.sleep(5)
                    os.system("cls")
            elif contains_base64(result):
                success("Successfully decompiled Base64 string: " + result)


    except Exception as e:
        error(f"Error fetching or processing file: {e}")


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
                fams = None
                score = None

                file_name_div = report.find('div', class_='column-target')
                file_name = file_name_div.text.strip() if file_name_div else "Unknown file"

                score_div = report.find('div', class_='column-score')
                score_text = score_div.find('div', class_='score').text if score_div else None
                score = float(score_text.strip()) if score_text else None

                tags_div = report.find('div', class_='column-tags')
                tags = [tag.text.strip() for tag in tags_div.find_all('span')] if tags_div else []

                time_uploaded = report.find('div', class_="column-created").text.replace('UTC', '\n').strip()
                fams_element = report.find('span', class_="rose")

                if fams_element:
                    fams = fams_element.text
                else:
                    fams = "No family"

                os.system("cls")

                if score is not None and score > 6:
                    log_entries = [
                        (f"{Fore.LIGHTBLUE_EX}ID:{Style.RESET_ALL}", report_id),
                        (f"{Fore.LIGHTCYAN_EX}SHA256:{Style.RESET_ALL}", file_name),
                        (f"{Fore.LIGHTMAGENTA_EX}Name:{Style.RESET_ALL}", file_name),
                        (f"{Fore.LIGHTRED_EX}Score:{Style.RESET_ALL}", score),
                        (f"{Fore.LIGHTGREEN_EX}Family:{Style.RESET_ALL}", fams),
                        (f"{Fore.LIGHTCYAN_EX}Tags:{Style.RESET_ALL}", ', '.join(tags) if tags else 'No tags'),
                        (f"{Fore.LIGHTYELLOW_EX}Time Scraped:{Style.RESET_ALL}", current_time),
                        (f"{Fore.LIGHTMAGENTA_EX}Time Uploaded:{Style.RESET_ALL}", time_uploaded + "\n")
                    ]

                    for title, value in log_entries:
                        newlog(f"{title} {Fore.WHITE}{value}{Style.RESET_ALL}")

                executor.submit(lambda: asyncio.run(process_submission(report_id, file_name, fams, score, time_uploaded, tags)))

                processed_ids.add(report_id)

                if 'discordrat' in tags:
                    success(f"Found DiscordRAT in submission https://tria.ge/{report_id}")

def main():
    while True:
        check_for_new_submissions()
        info("Waiting for new submissions..")
        time.sleep(0.5)


if __name__ == "__main__":
    main()
