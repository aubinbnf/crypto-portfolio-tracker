from fastapi import FastAPI
from typing import List
from portfolio_service import PortfolioService
from core.aggregator import Aggregator
from core.models import Balance, TotalsResponse, SnapshotModel

# python -m uvicorn main:app --reload
app = FastAPI(title="Crypto Portfolio API", version="0.1.0")
service = PortfolioService()
agg = Aggregator()

@app.get("/balances", response_model=List[Balance])
def get_balances():
    balances = agg.get_all_balances()
    return balances

@app.get("/totals", response_model=TotalsResponse)
def get_totals():
    balances = agg.get_all_balances()
    totals = agg.aggregate_by_asset(balances)
    totals = agg.add_usd_values(totals)
    total_usd = sum(t["value_usd"] for t in totals if t["value_usd"])
    return {"totals": totals, "total_usd": total_usd}

@app.post("/snapshots", response_model=SnapshotModel)
def create_snapshot():
    snapshot = service.create_snapshot()
    latest = service.get_latest_snapshot()
    return latest

@app.get("/snapshots/latest", response_model=SnapshotModel)
def get_latest_snapshot():
    latest = service.get_latest_snapshot()
    if not latest:
        return {"id": 0, "fetched_at": None, "items": []}
    return latest

@app.get("/health")
def health_check():
    return {"status": "ok"}
