import requests
import time
from colorama import Fore, init
import os

init(autoreset=True)

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

banner = """
██╗░░░░░░░██╗███████╗██████╗░██╗░░██╗░█████╗░░█████╗░██╗░░██╗
██║░░██╗░░██║██╔════╝██╔══██╗██║░░██║██╔══██╗██╔══██╗██║░██╔╝
╚██╗████╗██╔╝█████╗░░██████╦╝███████║██║░░██║██║░░██║█████═╝░
░████╔═████║░██╔══╝░░██╔══██╗██╔══██║██║░░██║██║░░██║██╔═██╗░
░╚██╔╝░╚██╔╝░███████╗██████╦╝██║░░██║╚█████╔╝╚█████╔╝██║░╚██╗
░░╚═╝░░░╚═╝░░╚══════╝╚═════╝░╚═╝░░╚═╝░╚════╝░░╚════╝░╚═╝░░╚═╝
                                                  
"""

def spam_single_webhook(webhook_url, message, delay=0.33):
    print(Fore.YELLOW + f"Spamming webhook: {webhook_url}")
    while True:
        try:
            data = {"content": message}
            res = requests.post(webhook_url, json=data)
            if res.status_code == 204:
                print(Fore.GREEN + "Message sent!")
            else:
                print(Fore.RED + f"Failed to send message: {res.status_code}")
            time.sleep(delay)
        except KeyboardInterrupt:
            print(Fore.RED + "\nStopped by user.")
            break
        except Exception as e:
            print(Fore.RED + f"Error: {e}")
            break

def spam_multiple_webhooks(webhook_file, message, delay=0.33):
    if not os.path.exists(webhook_file):
        print(Fore.RED + f"Webhook file '{webhook_file}' not found!")
        return

    with open(webhook_file, "r") as f:
        webhooks = [line.strip() for line in f if line.strip()]

    print(Fore.YELLOW + f"Loaded {len(webhooks)} webhooks from {webhook_file}")
    print(Fore.YELLOW + "Starting spam on multiple webhooks...")

    while True:
        for webhook_url in webhooks:
            try:
                data = {"content": message}
                res = requests.post(webhook_url, json=data)
                if res.status_code == 204:
                    print(Fore.GREEN + f"Message sent on {webhook_url}")
                else:
                    print(Fore.RED + f"Failed on {webhook_url}: {res.status_code}")
                time.sleep(delay)
            except KeyboardInterrupt:
                print(Fore.RED + "\nStopped by user.")
                return
            except Exception as e:
                print(Fore.RED + f"Error on {webhook_url}: {e}")

def mass_delete_webhooks(token, guild_id):
    headers = {"Authorization": token}
    url = f"https://discord.com/api/v10/guilds/{guild_id}/webhooks"
    
    try:
        res = requests.get(url, headers=headers)
        if res.status_code != 200:
            print(Fore.RED + f"Failed to get webhooks: {res.status_code} - {res.text}")
            return

        webhooks = res.json()
        print(Fore.YELLOW + f"Found {len(webhooks)} webhooks. Deleting all...")

        for webhook in webhooks:
            wh_id = webhook['id']
            del_res = requests.delete(f"https://discord.com/api/v10/webhooks/{wh_id}", headers=headers)
            if del_res.status_code in [200, 204]:
                print(Fore.GREEN + f"Deleted webhook {webhook['name']} ({wh_id})")
            else:
                print(Fore.RED + f"Failed to delete webhook {webhook['name']} ({wh_id}): {del_res.status_code}")
            time.sleep(0.5)

    except KeyboardInterrupt:
        print(Fore.RED + "\nOperation interrupted by user.")
    except Exception as e:
        print(Fore.RED + f"Error: {e}")

def main():
    clear()
    print(Fore.BLUE + banner)
    print(Fore.YELLOW + "[1] Spam 1 Webhook")
    print(Fore.YELLOW + "[2] Spam multiple Webhooks (from webhooks.txt)")
    print(Fore.YELLOW + "[3] Mass Delete Webhooks (requires bot token and guild ID)")
    print(Fore.YELLOW + "[0] Return")

    choice = input(f"{Fore.GREEN}Choose an option: ").strip()
    if choice == "1":
        webhook_url = input(f"{Fore.GREEN}Enter webhook URL: ").strip()
        message = input(f"{Fore.GREEN}Enter message to spam: ").strip()
        print(Fore.YELLOW + "Spamming... Press Ctrl+C to stop.")
        spam_single_webhook(webhook_url, message)
    elif choice == "2":
        message = input(f"{Fore.GREEN}Enter message to spam: ").strip()
        print(Fore.YELLOW + "Spamming all webhooks from webhooks.txt... Press Ctrl+C to stop.")
        spam_multiple_webhooks("webhooks.txt", message)
    elif choice == "3":
        token = input(f"{Fore.GREEN}Enter bot token: ").strip()
        guild_id = input(f"{Fore.GREEN}Enter guild ID: ").strip()
        if not token or not guild_id:
            print(Fore.RED + "Token and Guild ID are required!")
            input("Press Enter to continue...")
        else:
            mass_delete_webhooks(token, guild_id)
            input("Press Enter to continue...")
    elif choice == "0":
        return
    else:
        print(Fore.RED + "Invalid option.")
        input("Press Enter to continue...")

if __name__ == "__main__":
    main()
