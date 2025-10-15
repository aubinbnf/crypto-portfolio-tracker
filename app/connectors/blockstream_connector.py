import os, requests
from dotenv import load_dotenv
from datetime import datetime
from app.connectors import Connector

load_dotenv()

class BlockstreamConnector(Connector):
    def __init__(self):
        self.addresses = os.getenv("BTC_ADDRESSES", "").split(",")
        if not self.addresses:
            raise ValueError("BTC_ADDRESSES is missing")

    def fetch_balances(self):
        balances = []
        for address in self.addresses:
            address = address.strip()
            if not address:
                continue

            url = f"https://blockstream.info/api/address/{address}"
            r = requests.get(url, timeout=10)
            r.raise_for_status()
            data = r.json()

            funded = data["chain_stats"]["funded_txo_sum"]
            spent = data["chain_stats"]["spent_txo_sum"]
            balance_sats = funded - spent
            balance_btc = balance_sats / 1e8

            balances.append({
                "source": "blockstream",
                "chain": "bitcoin",
                "asset": "BTC",
                "balance": balance_btc,
                "address": address,
                "fetched_at": datetime.utcnow().isoformat()
            })
        return balances