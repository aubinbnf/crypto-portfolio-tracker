import os, requests
from dotenv import load_dotenv
from datetime import datetime
from connectors.base import Connector  # si tu as déjà défini une base abstraite

load_dotenv()

class BlockstreamConnector(Connector):
    def __init__(self):
        self.address = os.getenv("BTC_ADDRESS")
        if not self.address:
            raise ValueError("BTC_ADDRESS is missing")

    def fetch_balances(self):
        url = f"https://blockstream.info/api/address/{self.address}"
        r = requests.get(url, timeout=10)
        r.raise_for_status()
        data = r.json()

        funded = data["chain_stats"]["funded_txo_sum"]
        spent = data["chain_stats"]["spent_txo_sum"]
        balance_sats = funded - spent
        balance_btc = balance_sats / 1e8

        return [{
            "source": "blockstream",
            "chain": "bitcoin",
            "asset": "BTC",
            "balance": balance_btc,
            "address": self.address,
            "fetched_at": datetime.utcnow().isoformat()
        }]