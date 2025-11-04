from datetime import datetime
from sqlalchemy.orm import Session
from models import Snapshot, SnapshotItem
import json

class SnapshotRepository:
    def __init__(self, db: Session):
        self.db = db

    def create_snapshot(self, balances: list, meta: dict | None = None):
        snapshot = Snapshot(
            fetched_at=datetime.utcnow(),
            meta=json.dumps(meta or {})
        )
        for b in balances:
            item = SnapshotItem(
                source=b.get("source"),
                chain=b.get("chain"),
                asset=b.get("asset"),
                balance=b.get("balance"),
                address=b.get("address"),
                price_usd=b.get("price_usd"),
                value_usd=b.get("value_usd"),
                raw=json.dumps(b)
            )
            snapshot.items.append(item)

        self.db.add(snapshot)
        self.db.commit()
        self.db.refresh(snapshot)
        return snapshot

    def get_latest(self):
        return self.db.query(Snapshot).order_by(Snapshot.fetched_at.desc()).first()

    def get_all(self, limit: int = 100):
        """Get all snapshots ordered by date (most recent first)"""
        return self.db.query(Snapshot).order_by(Snapshot.fetched_at.desc()).limit(limit).all()

    def get_items_for_snapshot(self, snapshot_id: int):
        return self.db.query(SnapshotItem).filter(SnapshotItem.snapshot_id == snapshot_id).all()