from db import SessionLocal
from repositories.snapshot_repository import SnapshotRepository
from core.aggregator import Aggregator

class PortfolioService:
    def __init__(self):
        self.db = SessionLocal()
        self.repo = SnapshotRepository(self.db)
        self.aggregator = Aggregator()

    def create_snapshot(self):
        balances = self.aggregator.get_all_balances()
        totals = self.aggregator.add_usd_values(self.aggregator.aggregate_by_asset(balances))
        snapshot = self.repo.create_snapshot(totals)
        return snapshot

    def get_latest_snapshot(self):
        snapshot = self.repo.get_latest()
        if not snapshot:
            return None
        items = self.repo.get_items_for_snapshot(snapshot.id)
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