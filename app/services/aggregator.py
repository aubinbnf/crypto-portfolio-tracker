import requests
import yaml
from app.connectors import EtherscanConnector, BlockstreamConnector, BinanceConnector, CoinGeckoConnector
from collections import defaultdict

class Aggregator:
    def __init__(self, connectors=None, config_path="app/config/assets.yaml"):
        with open(config_path, "r") as f:
            self.config = yaml.safe_load(f)
        self.asset_map = self.config.get("asset_map", {})
        
        self.connectors = connectors or [
            EtherscanConnector(),
            BlockstreamConnector(),
            BinanceConnector()
        ]

        self.coingecko = CoinGeckoConnector()

    def get_all_balances(self):
        balances = []
        for c in self.connectors:
            result = c.fetch_balances()
            balances.extend(result if isinstance(result, list) else [result])
        return balances

    def aggregate_by_asset(self, balances):
        totals = defaultdict(float)

        for b in balances:
            asset = b["asset"]
            totals[asset] += b["balance"]

        return [{"asset": asset, "total_balance": balance} for asset, balance in totals.items()]

    def fetch_prices(self, assets, vs="usd"):
        ids = [self.asset_map[a] for a in assets if a in self.asset_map]
        price = self.coingecko.get_price(ids, vs)
        return price

    def add_usd_values(self, totals):
        assets = [t["asset"] for t in totals]
        prices = self.fetch_prices(assets)
        for t in totals:
            asset = t["asset"]
            cg_id = self.asset_map.get(asset)
            if cg_id and cg_id in prices:
                price = prices[cg_id]["usd"]
                t["price_usd"] = price
                t["value_usd"] = t["total_balance"] * price
            else:
                t["price_usd"] = None
                t["value_usd"] = None
        return totals