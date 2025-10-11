from app.services import PortfolioService

service = PortfolioService()

snapshot = service.create_snapshot()
print(f"✅ Snapshot {snapshot.id} enregistré avec {len(snapshot.items)} items.")

latest = service.get_latest_snapshot()
print(f"\n🕒 Dernier snapshot ({latest['fetched_at']}):")
for item in latest["items"]:
    print(f" - {item['asset']}: {item['balance']} ({item['value_usd']} USD)")
