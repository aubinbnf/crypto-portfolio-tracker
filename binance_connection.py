from binance.client import Client
from dotenv import load_dotenv
import os

load_dotenv()
api_key = os.getenv("BINANCE_API_KEY")
api_secret = os.getenv("BINANCE_API_SECRET")

# Connection
client = Client(api_key, api_secret)

# Get account balances
account_info = client.get_account()

print("Assets held :")
for asset in account_info['balances']:
    free = float(asset['free'])
    locked = float(asset['locked'])
    if free + locked > 0:
        print(f"{asset['asset']}: Free = {free}, Blocked = {locked}")