import os, requests
from dotenv import load_dotenv

load_dotenv()
ADDRESS = os.getenv("BTC_ADDRESS")

url = f"https://blockstream.info/api/address/{ADDRESS}"
r = requests.get(url, timeout=10)
r.raise_for_status()
data = r.json()

funded = data["chain_stats"]["funded_txo_sum"]
spent = data["chain_stats"]["spent_txo_sum"]
balance_sats = funded - spent
balance_btc = balance_sats / 1e8

print(f"BTC balance: {balance_btc} BTC")