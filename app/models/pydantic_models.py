from pydantic import BaseModel, Field
from datetime import datetime
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

class SnapshotItemModel(BaseModel):
    asset: str
    balance: float | None = Field(default=0.0)
    value_usd: float | None = None
    source: str | None = None
    chain: str | None = None

class SnapshotModel(BaseModel):
    id: int
    fetched_at: datetime
    items: List[SnapshotItemModel]

    class Config:
        orm_mode = True
