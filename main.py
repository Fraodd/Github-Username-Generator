import requests
from colorama import Fore, init
from random import choices, choice
import time
import os

init(autoreset=True)

# List of colors for terminal output
colors = [
    Fore.RED,
    Fore.GREEN,
    Fore.YELLOW,
    Fore.BLUE,
    Fore.MAGENTA,
    Fore.CYAN,
]

# Function to write available usernames to a file
def write_to_file(username):
    filename = 'Available.txt'
    with open(filename, 'a') as file:
        file.write(f"{username}\n")

def check(username_length):
    print(Fore.CYAN + f"[!] Checking usernames with {username_length} characters...\n")
    
    retry_attempt = 0
    max_retries = 5

    while True:
        # Generate a random username based on the user-specified length
        username = ''.join(choices('ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789', k=username_length))
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36',
        }

        # URL to check if the GitHub profile exists
        url = f'https://github.com/{username}'

        try:
            response = requests.get(url, headers=headers)
            
            if response.status_code == 200:
                # Profile exists, username is taken
                print(f"{Fore.RED}[-] {username} Taken")
                retry_attempt = 0  # Reset retry count after a successful check
            elif response.status_code == 404:
                # Profile not found, username is available
                print(f"{Fore.GREEN}[+] {username} Available")
                write_to_file(username)  # Write available username to file
                retry_attempt = 0  # Reset retry count after a successful check
            elif response.status_code == 429:
                # Too many requests, implement backoff
                print(Fore.YELLOW + "[!] Rate limit exceeded. Retrying after delay...")
                retry_attempt += 1
                if retry_attempt > max_retries:
                    print(Fore.RED + "[!] Max retries exceeded. Exiting...")
                    break
                # Exponential backoff
                time.sleep(2 ** retry_attempt)
            else:
                print(f"{Fore.YELLOW}[!] Unexpected Status Code: {response.status_code}")
                retry_attempt = 0  # Reset retry count on unexpected status code
                
        except requests.exceptions.HTTPError as http_err:
            print(f"{Fore.RED}[!] HTTP error occurred: {http_err}")
            retry_attempt = 0  # Reset retry count on HTTP error
        except requests.exceptions.ConnectionError as conn_err:
            print(f"{Fore.RED}[!] Connection error occurred: {conn_err}")
            retry_attempt = 0  # Reset retry count on connection error
        except requests.exceptions.Timeout as timeout_err:
            print(f"{Fore.RED}[!] Timeout error occurred: {timeout_err}")
            retry_attempt = 0  # Reset retry count on timeout error
        except requests.RequestException as req_err:
            print(f"{Fore.RED}[!] An error occurred: {req_err}")
            retry_attempt = 0  # Reset retry count on general request error
        except requests.exceptions.TooManyRedirects as redirect_err:
            print(f"{Fore.RED}[!] Too many redirects: {redirect_err}")
            retry_attempt = 0  # Reset retry count on too many redirects

        # Shortened sleep to 1 second for faster iteration, adjust if necessary
        time.sleep(1)

def main_menu():
    # Banner in purple
    banner = """
                         _       _     ____                     _ 
                        | |     | |   / / _|                   | |
  __ _ _   _ _ __  ___  | | ___ | |  / / |_ _ __ __ _  ___   __| |
 / _` | | | | '_ \/ __| | |/ _ \| | / /|  _| '__/ _` |/ _ \ / _` |
| (_| | |_| | | | \__ \_| | (_) | |/ / | | | | | (_| | (_) | (_| |
 \__, |\____|_| |_|___(_)_|\___/|_/_/  |_| |_|  \____|\___/ \____|
  __/ |                                                           
 |___/                                                            
    """
    print(Fore.MAGENTA + banner)  # Print banner in purple
    print(Fore.CYAN + "--- GitHub Username Checker ---\n")
    print("1. Start checking usernames")
    print("2. Exit\n")

    while True:
        choice = input(Fore.CYAN + "Enter your choice (1 or 2): ").strip()

        if choice == '1':
            while True:
                try:
                    username_length = int(input(Fore.CYAN + "Enter the number of characters for the usernames (2-20): ").strip())
                    if 2 <= username_length <= 20:
                        check(username_length)
                    else:
                        print(Fore.RED + "[!] Please enter a number between 2 and 20.")
                except ValueError:
                    print(Fore.RED + "[!] Invalid input. Please enter a valid number.")
        elif choice == '2':
            print(Fore.CYAN + "\n[!] Exiting the program. Goodbye!")
            break
        else:
            print(Fore.RED + "[!] Invalid choice. Please select 1 or 2.")

if __name__ == "__main__":
    try:
        main_menu()
    except KeyboardInterrupt:
        print(Fore.CYAN + "\n[!] Program stopped by user.")
