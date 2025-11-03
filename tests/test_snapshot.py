import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from services import PortfolioService

service = PortfolioService()

snapshot = service.create_snapshot()
print(f"Snapshot {snapshot.id} saved with {len(snapshot.items)} items.")

latest = service.get_latest_snapshot()
print(f"\nLast snapshot ({latest['fetched_at']}):")
for item in latest["items"]:
    print(f" - {item['asset']}: {item['balance']} ({item['value_usd']} USD)")
