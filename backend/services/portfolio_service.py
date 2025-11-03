from models import SessionLocal
from repositories import SnapshotRepository
import yaml
from connectors import EtherscanConnector, BlockstreamConnector, BinanceConnector, CoinGeckoConnector
from collections import defaultdict

class PortfolioService:
    def __init__(self, connectors=None, config_path="config/assets.yaml"):
        self.db = SessionLocal()
        self.repo = SnapshotRepository(self.db)

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
    
    def fetch_prices(self, assets, vs="usd"):
        ids = [self.asset_map[a] for a in assets if a in self.asset_map]
        price = self.coingecko.get_price(ids, vs)
        return price

    def add_usd_values(self, balances):
        assets = list(set(b["asset"] for b in balances))
        prices = self.fetch_prices(assets)
        for b in balances:
            asset = b["asset"]
            cg_id = self.asset_map.get(asset)
            if cg_id and cg_id in prices:
                price = prices[cg_id]["usd"]
                b["price_usd"] = price
                b["value_usd"] = b["balance"] * price
            else:
                b["price_usd"] = None
                b["value_usd"] = None
        return balances
    
    def aggregate_by_asset(self, balances):
        totals = defaultdict(float)

        for b in balances:
            asset = b["asset"]
            totals[asset] += b["balance"]

        return [{"asset": asset, "balance": balance} for asset, balance in totals.items()]

    def create_snapshot(self):
        balances = self.get_all_balances()
        balances_with_prices = self.add_usd_values(balances)
        snapshot = self.repo.create_snapshot(balances_with_prices)
        return snapshot

    def get_latest_snapshot(self):
        snapshot = self.repo.get_latest()
        if not snapshot:
            return None
        items = self.repo.get_items_for_snapshot(snapshot.id)
        print(items[0].asset)
        return {
            "id": snapshot.id,
            "fetched_at": snapshot.fetched_at,
            "items": [
                {
                    "asset": i.asset,
                    "balance": i.balance,
                    "value_usd": i.value_usd,
                    "source": i.source,
                    "chain": i.chain,
                }
                for i in items
            ]
        }