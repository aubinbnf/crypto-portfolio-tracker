import os
from binance.client import Client
from dotenv import load_dotenv
from datetime import datetime
from connectors import Connector

load_dotenv()

class BinanceConnector(Connector):
    def __init__(self):
        self.api_key = os.getenv("BINANCE_API_KEY")
        self.api_secret = os.getenv("BINANCE_API_SECRET")

        if not self.api_key or not self.api_secret:
            raise ValueError("BINANCE_API_KEY or BINANCE_API_SECRET is missing")

        self.client = Client(self.api_key, self.api_secret)

    def fetch_balances(self):
        account_info = self.client.get_account()

        balances = []
        for asset in account_info["balances"]:
            free = float(asset["free"])
            locked = float(asset["locked"])
            total = free + locked
            if total > 0:
                balances.append({
                    "source": "binance",
                    "chain": None,
                    "asset": asset["asset"],
                    "balance": total,
                    "address": None,
                    "fetched_at": datetime.utcnow().isoformat()
                })
        return balances