import os
from fastapi import FastAPI
from typing import List
from services import PortfolioService
from models import Balance, TotalsResponse, SnapshotModel
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

load_dotenv()

# python -m uvicorn main:app --reload
app = FastAPI(title="Crypto Portfolio API", version="0.1.0")

# CORS Management - configurable via environment variable
cors_origins = os.getenv("CORS_ORIGINS", "http://localhost:3000")
# Split by comma and strip whitespace from each origin
allowed_origins = [origin.strip() for origin in cors_origins.split(",")]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

print(f"CORS enabled for origins: {', '.join(allowed_origins)}")

service = PortfolioService()

@app.get("/balances", response_model=List[Balance])
def get_balances():
    balances = service.get_all_balances()
    return balances

@app.get("/totals", response_model=TotalsResponse)
def get_totals():
    balances = service.get_all_balances()
    totals = service.aggregate_by_asset(balances)
    totals = service.add_usd_values(totals)
    total_usd = sum(t["value_usd"] for t in totals if t["value_usd"])
    return {"totals": totals, "total_usd": total_usd}

@app.get("/totals/cached", response_model=TotalsResponse)
def get_totals_cached():
    """
    Get totals from latest snapshot in DB (fast, no external API calls).
    Use this for initial page load. Use POST /snapshots to refresh data.
    """
    return service.get_totals_from_cache()

@app.post("/snapshots", response_model=SnapshotModel)
def create_snapshot():
    service.create_snapshot()
    latest = service.get_latest_snapshot()
    return latest

@app.get("/snapshots/latest", response_model=SnapshotModel)
def get_latest_snapshot():
    latest = service.get_latest_snapshot()
    if not latest:
        return {"id": 0, "fetched_at": None, "items": []}
    return latest

@app.get("/snapshots", response_model=List[SnapshotModel])
def get_all_snapshots(limit: int = 30):
    """Get all snapshots history (limited to last 30 by default)"""
    snapshots = service.get_all_snapshots(limit=limit)
    return snapshots

@app.get("/health")
def health_check():
    return {"status": "ok"}
