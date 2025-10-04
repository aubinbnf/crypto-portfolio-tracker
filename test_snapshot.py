# test_snapshot.py
from portfolio_service import PortfolioService

service = PortfolioService()

# Créer un nouveau snapshot
snapshot = service.create_snapshot()
print(f"✅ Snapshot {snapshot.id} enregistré avec {len(snapshot.items)} items.")

# Récupérer le dernier snapshot
latest = service.get_latest_snapshot()
print(f"\n🕒 Dernier snapshot ({latest['fetched_at']}):")
for item in latest["items"]:
    print(f" - {item['asset']}: {item['balance']} ({item['value_usd']} USD)")
