import os
import requests
import threading
from colorama import Fore, init

init(autoreset=True)

REPORT_BANNER = r"""
███╗░░░███╗░█████╗░░██████╗░██████╗  ██████╗░███████╗██████╗░░█████╗░██████╗░████████╗
████╗░████║██╔══██╗██╔════╝██╔════╝  ██╔══██╗██╔════╝██╔══██╗██╔══██╗██╔══██╗╚══██╔══╝
██╔████╔██║███████║╚█████╗░╚█████╗░  ██████╔╝█████╗░░██████╔╝██║░░██║██████╔╝░░░██║░░░
██║╚██╔╝██║██╔══██║░╚═══██╗░╚═══██╗  ██╔══██╗██╔══╝░░██╔═══╝░██║░░██║██╔══██╗░░░██║░░░
██║░╚═╝░██║██║░░██║██████╔╝██████╔╝  ██║░░██║███████╗██║░░░░░╚█████╔╝██║░░██║░░░██║░░░
╚═╝░░░░░╚═╝╚═╝░░╚═╝╚═════╝░╚═════╝░  ╚═╝░░╚═╝╚══════╝╚═╝░░░░░░╚════╝░╚═╝░░╚═╝░░░╚═╝░░░  

"""

DEFAULT_REPORT_REASON = "Inappropriate content"

def clear():
    os.system("cls" if os.name == "nt" else "clear")

def report(token, guild_id, channel_id, message_id, reason):
    responses = {
        '401: Unauthorized': f'{Fore.RED}Invalid Discord token.',
        'Missing Access': f'{Fore.RED}Missing access to channel or guild.',
        'You need to verify your account in order to perform this action.': f'{Fore.RED}Unverified account.'
    }

    r = requests.post(
        'https://discord.com/api/v8/report',
        json={
            'channel_id': channel_id,
            'message_id': message_id,
            'guild_id': guild_id,
            'reason': reason
        },
        headers={
            'Authorization': token,
            'Content-Type': 'application/json',
            'User-Agent': 'Discord/21295 CFNetwork/1128.0.1 Darwin/19.6.0'
        }
    )

    if r.status_code == 201:
        print(Fore.MAGENTA + "[+] Report sent successfully.\n")
    elif r.status_code in (401, 403):
        msg = r.json().get('message', 'Unknown error')
        print(responses.get(msg, f"{Fore.RED}Access denied or invalid credentials.\n"))
    else:
        print(Fore.RED + f"[!] Error {r.status_code}: {r.text}\n")

def mass_report(token, guild_id, channel_id, message_id, reason):
    for _ in range(100):  # Limit number of threads to prevent abuse / crash
        threading.Thread(target=report, args=(token, guild_id, channel_id, message_id, reason)).start()

def main():
    clear()
    print(Fore.CYAN + REPORT_BANNER)

    token = input(Fore.YELLOW + "Enter your Discord token: ").strip()
    guild_id = input(Fore.YELLOW + "Enter the server (guild) ID: ").strip()
    channel_id = input(Fore.YELLOW + "Enter the channel ID: ").strip()
    message_id = input(Fore.YELLOW + "Enter the message ID: ").strip()

    reason = input(Fore.YELLOW + f"Enter report reason (default: {DEFAULT_REPORT_REASON}): ").strip()
    if not reason:
        reason = DEFAULT_REPORT_REASON

    print(Fore.GREEN + "\n[+] Starting mass report...\n")
    mass_report(token, guild_id, channel_id, message_id, reason)

if __name__ == "__main__":
    main()
