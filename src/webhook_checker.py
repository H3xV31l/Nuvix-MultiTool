import os
from colorama import Fore, init

init(autoreset=True)

WEBHOOK_BANNER = r"""
██╗░░░░░░░██╗███████╗██████╗░██╗░░██╗░█████╗░░█████╗░██╗░░██╗
██║░░██╗░░██║██╔════╝██╔══██╗██║░░██║██╔══██╗██╔══██╗██║░██╔╝
╚██╗████╗██╔╝█████╗░░██████╦╝███████║██║░░██║██║░░██║█████═╝░
░████╔═████║░██╔══╝░░██╔══██╗██╔══██║██║░░██║██║░░██║██╔═██╗░
░╚██╔╝░╚██╔╝░███████╗██████╦╝██║░░██║╚█████╔╝╚█████╔╝██║░╚██╗
░░╚═╝░░░╚═╝░░╚══════╝╚═════╝░╚═╝░░╚═╝░╚════╝░░╚════╝░╚═╝░░╚═╝
"""

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def webhook_checker(url):
    print()
    if url.startswith("https://discord.com/api/webhooks/"):
        print(Fore.GREEN + "✅ Webhook URL looks valid!")
    else:
        print(Fore.RED + "❌ Invalid webhook URL!")

def main():
    clear()
    print(Fore.CYAN + WEBHOOK_BANNER)
    print()
    url = input(Fore.YELLOW + "Enter webhook URL to check: ").strip()
    if not url:
        print(Fore.RED + "No URL provided.")
        return
    webhook_checker(url)
    print()
    input(Fore.MAGENTA + "Press Enter to return to the menu...")

if __name__ == "__main__":
    main()
