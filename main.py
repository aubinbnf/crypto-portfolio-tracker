from fastapi import FastAPI
from typing import List
from core.aggregator import Aggregator
from core.models import Balance, TotalsResponse

# python -m uvicorn main:app --reload
app = FastAPI(title="Crypto Portfolio API", version="0.1.0")
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

@app.get("/health")
def health_check():
    return {"status": "ok"}
