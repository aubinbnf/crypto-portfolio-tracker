import os, requests
from dotenv import load_dotenv
from datetime import datetime
from connectors.base import Connector

load_dotenv()

class EtherscanConnector(Connector):
    def __init__(self):
        self.api_key = os.getenv("ETHERSCAN_API_KEY")
        self.address = os.getenv("ETH_ADDRESS")

        if not self.api_key or not self.address:
            raise ValueError("ETHERSCAN_API_KEY or ETH_ADDRESS is missing")

    def fetch_balances(self):
        r = requests.get(
            "https://api.etherscan.io/v2/api?chainid=1",
            params={
                "module": "account",
                "action": "balance",
                "address": self.address,
                "tag": "latest",
                "apikey": self.api_key
            },
            timeout=10
        )
        r.raise_for_status()
        data = r.json()
        wei = int(data["result"])
        eth = wei / 10**18

        return [{
            "source": "etherscan",
            "chain": "ethereum",
            "asset": "ETH",
            "balance": eth,
            "address": self.address,
            "fetched_at": datetime.utcnow().isoformat()
        }]