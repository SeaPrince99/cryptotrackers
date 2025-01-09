import time
import requests

def get_eth_price():
    try:
        response = requests.get('https://api.coingecko.com/api/v3/simple/price?ids=ethereum&vs_currencies=usd')
        response.raise_for_status()
        data = response.json()
        return data['ethereum']['usd']
    except requests.RequestException as e:
        print(f"Error fetching ETH price: {e}")
        return None

def track_eth_price(interval=10):
    last_price = None
    while True:
        price = get_eth_price()
        if price is not None:
            if price != last_price:
                print(f"ETH Price: ${price}")
                last_price = price
        else:
            print("Failed to fetch ETH price")
        time.sleep(interval)

if __name__ == "__main__":
    track_eth_price()