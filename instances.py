import os, time
import colorama
from colorama import Fore

colorama.init(autoreset=True)

def info(text):
    print(f"{Fore.CYAN}[{Fore.CYAN}INFO{Fore.CYAN}]{Fore.WHITE} > " + text)

def error(text):
    print(f"{Fore.RED}[{Fore.RED}ERROR{Fore.RED}]{Fore.WHITE} > " + text)

def success(text):
    print(f"{Fore.LIGHTGREEN_EX}[{Fore.LIGHTGREEN_EX}SUCCESS{Fore.LIGHTGREEN_EX}]{Fore.WHITE} > " + text)

def warning(text):
    print(f"{Fore.YELLOW}[{Fore.YELLOW}WARNING{Fore.YELLOW}]{Fore.WHITE} > " + text)

def newlog(text):
    print(f"{Fore.GREEN}[{Fore.LIGHTGREEN_EX}NEW LOG{Fore.GREEN}]{Fore.WHITE} > " + text)
def monokai(text):
    print(f"{Fore.LIGHTYELLOW_EX}[MONOKAI]{Fore.WHITE} > {text}")
def info(text):
    print(f"{Fore.CYAN}[INFO]{Fore.WHITE} > {text}")
