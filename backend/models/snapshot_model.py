from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from datetime import datetime
from models import Base

class Snapshot(Base):
    __tablename__ = "snapshots"
    id = Column(Integer, primary_key=True, index=True)
    fetched_at = Column(DateTime, default=datetime.utcnow, index=True)
    meta = Column(Text, nullable=True)
    items = relationship("SnapshotItem", back_populates="snapshot", cascade="all, delete-orphan")

class SnapshotItem(Base):
    __tablename__ = "snapshot_items"
    id = Column(Integer, primary_key=True, index=True)
    snapshot_id = Column(Integer, ForeignKey("snapshots.id", ondelete="CASCADE"), index=True)
    source = Column(String, index=True)
    chain = Column(String, index=True)
    asset = Column(String, index=True) 
    balance = Column(Float)
    address = Column(String, nullable=True, index=True)
    price_usd = Column(Float, nullable=True)
    value_usd = Column(Float, nullable=True)
    raw = Column(Text, nullable=True)
    snapshot = relationship("Snapshot", back_populates="items")