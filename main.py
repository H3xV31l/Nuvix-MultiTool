import os
import sys
import time
import subprocess
from colorama import Fore, init
from pathlib import Path

init(autoreset=True)

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def banner():
    print(Fore.WHITE + """
███╗░░██╗██╗░░░██╗██╗░░░██╗██╗██╗░░██╗
████╗░██║██║░░░██║██║░░░██║██║╚██╗██╔╝
██╔██╗██║██║░░░██║╚██╗░██╔╝██║░╚███╔╝░
██║╚████║██║░░░██║░╚████╔╝░██║░██╔██╗░
██║░╚███║╚██████╔╝░░╚██╔╝░░██║██╔╝╚██╗
╚═╝░░╚══╝░╚═════╝░░░░╚═╝░░░╚═╝╚═╝░░╚═╝
""")

def tool_name(index):
    names = {
        1: "Token Nuker",
        2: "Webhook Spam",
        3: "Token Info",
        4: "Webhook Check",
        5: "DoS Attack",
        6: "Mass Report",
    }
    return names.get(index, "Soon")

def menu():
    total = 20
    rows = 4
    cols = total // rows
    col_width = 22

    for r in range(rows):
        line = ""
        for c in range(cols):
            index = r + c * rows + 1
            if index <= total:
                name = tool_name(index)
                cell = f"{index}. {name}"
                line += f"{cell:<{col_width}}"
        print(Fore.RED + line)
    print()

def main():
    tools = {
        "1": ("Token Nuker", Path("src/token_nuker.py")),
        "2": ("Webhook Spammer", Path("src/webhook_spammer.py")),
        "3": ("Token Info", Path("src/token_info.py")),
        "4": ("Webhook Checker", Path("src/webhook_checker.py")),
        "5": ("DoS Attack", Path("src/DOSAttack.py")),
        "6": ("Mass Report", Path("src/massreport.py")),
    }

    while True:
        try:
            clear()
            banner()
            menu()
            choice = input(Fore.YELLOW + "Choose an option (0 to exit): ").strip()

            if choice == "0":
                print(Fore.RED + "Exiting...")
                time.sleep(1)
                sys.exit()
            elif choice in tools:
                script_path = tools[choice][1]
                if script_path.exists():
                    subprocess.run([sys.executable, str(script_path)])
                else:
                    print(Fore.RED + f"Script {script_path.name} not found!")
                    input("Press Enter to continue...")
            elif choice.isdigit() and 1 <= int(choice) <= 20:
                print(Fore.BLUE + "Coming Soon...")
                input("Press Enter to continue...")
            else:
                print(Fore.RED + "Invalid option, try again.")
                input("Press Enter to continue...")
        except KeyboardInterrupt:
            print("\n" + Fore.RED + "Interrupted by user, exiting...")
            sys.exit()
        except Exception as e:
            print(Fore.RED + f"Unexpected error: {e}")
            input("Press Enter to continue...")

if __name__ == "__main__":
    main()
