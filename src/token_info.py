import requests
from colorama import Fore, init
import os

init(autoreset=True)

TOKEN_BANNER = r"""
████████╗░█████╗░██╗░░██╗███████╗███╗░░██╗     ██╗███╗░░██╗███████╗░█████╗░
╚══██╔══╝██╔══██╗██║░██╔╝██╔════╝████╗░██║     ██║████╗░██║██╔════╝██╔══██╗
░░░██║░░░██║░░██║█████═╝░█████╗░░██╔██╗██║     ██║██╔██╗██║█████╗░░██║░░██║
░░░██║░░░██║░░██║██╔═██╗░██╔══╝░░██║╚████║     ██║██║╚████║██╔══╝░░██║░░██║
░░░██║░░░╚█████╔╝██║░╚██╗███████╗██║░╚███║     ██║██║░╚███║██║░░░░░╚█████╔╝
░░░╚═╝░░░░╚════╝░╚═╝░░╚═╝╚══════╝╚═╝░░╚══╝     ╚═╝╚═╝░░╚══╝╚═╝░░░░░░╚════╝░
"""

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def get_user_info(token):
    headers = {
        "Authorization": token,
        "Content-Type": "application/json"
    }

    try:
        res = requests.get("https://discord.com/api/v9/users/@me", headers=headers)
        if res.status_code == 200:
            data = res.json()
            print(Fore.CYAN + f"ID: {data.get('id')}")
            print(Fore.CYAN + f"Username: {data.get('username')}#{data.get('discriminator')}")
            print(Fore.CYAN + f"Email: {data.get('email')}")
            print(Fore.CYAN + f"Verified: {data.get('verified')}")
            print(Fore.CYAN + f"Nitro: {'Yes' if data.get('premium_type') else 'No'}")
        else:
            print(Fore.RED + f"Invalid token or unauthorized. Status code: {res.status_code}")
    except Exception as e:
        print(Fore.RED + f"Error: {e}")

def main():
    clear()
    print(Fore.MAGENTA + TOKEN_BANNER)
    token = input(Fore.YELLOW + "Enter bot discord token: ").strip()

    if not token:
        print(Fore.RED + "No token entered.")
        return

    get_user_info(token)

    input(Fore.GREEN + "\nPress Enter to return to the menu...")

if __name__ == "__main__":
    main()

