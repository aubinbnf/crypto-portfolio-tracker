import os, requests
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("ETHERSCAN_API_KEY")
ADDRESS = os.getenv("ETH_ADDRESS")

r = requests.get(
    "https://api.etherscan.io/api",
    params={"module":"account","action":"balance","address":ADDRESS,"tag":"latest","apikey":API_KEY},
    timeout=10
)
r.raise_for_status()
data = r.json()
wei = int(data["result"])
eth = wei / 10**18
print(f"ETH balance: {eth} ETH")