from pydantic import BaseModel
from typing import Optional, List

class Balance(BaseModel):
    source: str
    chain: Optional[str] = None
    asset: str
    balance: float
    address: Optional[str] = None
    fetched_at: str

class Totals(BaseModel):
    asset: str
    total_balance: float
    price_usd: Optional[float] = None
    value_usd: Optional[float] = None

class TotalsResponse(BaseModel):
    totals: List[Totals]
    total_usd: float
