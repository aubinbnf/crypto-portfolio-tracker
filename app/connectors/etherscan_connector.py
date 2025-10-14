import os, requests
from dotenv import load_dotenv
from datetime import datetime
from app.connectors import Connector

load_dotenv()

class EtherscanConnector(Connector):
    def __init__(self):
        self.api_key = os.getenv("ETHERSCAN_API_KEY")
        self.addresses = os.getenv("ETH_ADDRESSES", "").split(",")

        if not self.api_key or not self.addresses:
            raise ValueError("ETHERSCAN_API_KEY or ETH_ADDRESSES is missing")

    def fetch_balances(self):
        balances = []
        for address in self.addresses:
            address = address.strip()
            if not address:
                continue
            r = requests.get(
                "https://api.etherscan.io/v2/api?chainid=1",
                params={
                    "module": "account",
                    "action": "balance",
                    "address": address,
                    "tag": "latest",
                    "apikey": self.api_key
                },
                timeout=10
            )
            r.raise_for_status()
            data = r.json()
            wei = int(data["result"])
            eth = wei / 10**18

            balances.append({
                "source": "etherscan",
                "chain": "ethereum",
                "asset": "ETH",
                "balance": eth,
                "address": address,
                "fetched_at": datetime.utcnow().isoformat()
            })
            
        return balances