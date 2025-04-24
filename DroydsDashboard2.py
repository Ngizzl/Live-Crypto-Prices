import requests
import datetime
import time
import os
from colorama import Fore, init

init(autoreset=True)

def get_crypto_data(symbol, retries=3):
    url = f"https://api.coingecko.com/api/v3/coins/{symbol}"
    for _ in range(retries):
        try:
            response = requests.get(url, timeout=10)
            data = response.json()
            if 'market_data' not in data:
                time.sleep(2)  # Avoid rate limits
                continue
            price = data['market_data']['current_price']['usd']
            change_24h = data['market_data']['price_change_percentage_24h']
            return price, change_24h
        except:
            time.sleep(1)
    return 0.0, 0.0  # Fallback if API fails

def get_time_zones():
    zones = {
        'EST': -5,
        'CST': -6,
        'MST': -7,
        'PST': -8,
        'AKST': -9,
        'HST': -10
    }
    time_data = {}
    for zone, offset in zones.items():
        now = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=offset)))
        time_data[zone] = now.strftime("%H:%M:%S")
    return time_data

def print_ascii_header():
    print(Fore.CYAN + r"""

████████▄     ▄████████  ▄██████▄  ▄██   ▄   ████████▄     ▄████████      ████████▄     ▄████████    ▄████████    ▄█    █▄    ▀█████████▄   ▄██████▄     ▄████████    ▄████████ ████████▄  
███   ▀███   ███    ███ ███    ███ ███   ██▄ ███   ▀███   ███    ███      ███   ▀███   ███    ███   ███    ███   ███    ███     ███    ███ ███    ███   ███    ███   ███    ███ ███   ▀███ 
███    ███   ███    ███ ███    ███ ███▄▄▄███ ███    ███   ███    █▀       ███    ███   ███    ███   ███    █▀    ███    ███     ███    ███ ███    ███   ███    ███   ███    ███ ███    ███ 
███    ███  ▄███▄▄▄▄██▀ ███    ███ ▀▀▀▀▀▀███ ███    ███   ███             ███    ███   ███    ███   ███         ▄███▄▄▄▄███▄▄  ▄███▄▄▄██▀  ███    ███   ███    ███  ▄███▄▄▄▄██▀ ███    ███ 
███    ███ ▀▀███▀▀▀▀▀   ███    ███ ▄██   ███ ███    ███ ▀███████████      ███    ███ ▀███████████ ▀███████████ ▀▀███▀▀▀▀███▀  ▀▀███▀▀▀██▄  ███    ███ ▀███████████ ▀▀███▀▀▀▀▀   ███    ███ 
███    ███ ▀███████████ ███    ███ ███   ███ ███    ███          ███      ███    ███   ███    ███          ███   ███    ███     ███    ██▄ ███    ███   ███    ███ ▀███████████ ███    ███ 
███   ▄███   ███    ███ ███    ███ ███   ███ ███   ▄███    ▄█    ███      ███   ▄███   ███    ███    ▄█    ███   ███    ███     ███    ███ ███    ███   ███    ███   ███    ███ ███   ▄███ 
████████▀    ███    ███  ▀██████▀   ▀█████▀  ████████▀   ▄████████▀       ████████▀    ███    █▀   ▄████████▀    ███    █▀    ▄█████████▀   ▀██████▀    ███    █▀    ███    ███ ████████▀  
             ███    ███                                                                                                                                              ███    ███            
     """)

def clear_data_section(lines_to_clear):
    # Move cursor up and clear the lines below the header
    print(f"\033[{lines_to_clear}A\033[J", end="")

def main():
    cryptos = {
        'bitcoin': 'BTC',
        'ethereum': 'ETH',
        'ripple': 'XRP',
        'solana': 'SOL',
        'monero': 'XMR',
        'cardano': 'ADA'
    }
    
    # Print header once
    print_ascii_header()
    
    # Calculate the number of lines in the data section to clear
    data_lines = len(cryptos) + 7 + len(get_time_zones())  # Crypto rows + title + separator + time zones + misc
    
    while True:
        time_data = get_time_zones()
        
        # Clear only the data section
        clear_data_section(data_lines)
        
        print(Fore.CYAN + "\n===################# LIVE CRYPTO PRICES ################===")
        print(Fore.YELLOW + "\nU.S. TIME ZONES:")
        for zone, t in time_data.items():
            print(f"{zone}: {t}")
        
        print(Fore.CYAN + "\n{:<8} {:<12} {:<10}".format("Coin", "Price (USD)", "24h Change"))
        print("-" * 32)
        
        for symbol, ticker in cryptos.items():
            price, change = get_crypto_data(symbol)
            color = Fore.GREEN if change >= 0 else Fore.RED
            direction = "▲" if change >= 0 else "▼"
            print(f"{ticker:<8} ${price:<11.2f} {color}{abs(change):<6.2f}% {direction}{Fore.RESET}")
        
        print(Fore.YELLOW + "\n[Ctrl+C] to exit | Updates every 30 sec...")
        time.sleep(30)  # Longer delay to avoid rate limits

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(Fore.RED + "\nDashboard closed.")