import time
from web3 import Web3

# Connect to an Ethereum node (e.g., Infura)
infura_url = "https://mainnet.infura.io/v3/a8b2dd8def1f44998129bd21ded2be0c"
web3 = Web3(Web3.HTTPProvider(infura_url))

# Uniswap V2 contract addresses and ABI
uniswap_v2_router_address = '0x7a250d5630B4cF539739dF2C5dAcb4c659F2488D'
uniswap_v2_router_abi = '[{"constant":true,"inputs":[{"internalType":"uint256","name":"amountIn","type":"uint256"},{"internalType":"address[]","name":"path","type":"address[]"}],"name":"getAmountsOut","outputs":[{"internalType":"uint256[]","name":"","type":"uint256[]"}],"payable":false,"stateMutability":"view","type":"function"}]'

# Create contract instance
uniswap_v2_router = web3.eth.contract(address=uniswap_v2_router_address, abi=uniswap_v2_router_abi)

def get_eth_price():
    try:
        # Define the path for ETH to USDC
        path = [
            web3.to_checksum_address('0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2'),  # WETH
            web3.to_checksum_address('0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48')   # USDC
        ]
        # Get the price of 1 ETH in USDC
        amounts = uniswap_v2_router.functions.getAmountsOut(web3.to_wei(1, 'ether'), path).call()
        eth_price_in_usdc = web3.from_wei(amounts[1], 'mwei')  # USDC has 6 decimal places
        return eth_price_in_usdc
    except Exception as e:
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
    if web3.is_connected():
        print("Connected to Ethereum node")
        track_eth_price()
    else:
        print("Failed to connect to Ethereum node")