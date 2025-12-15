# ============================================================================
# 🟣 Core4.AI – Market Intention Model
# Represents raw buyer demand (feature-first, product-agnostic)
# ============================================================================

from sqlalchemy import Column, Integer, String, Float, DateTime, JSON
from datetime import datetime
from db import Base


class MarketIntention(Base):
    __tablename__ = "market_intentions"

    id = Column(Integer, primary_key=True, index=True)

    # Raw & normalized intent
    feature_text = Column(String, nullable=False)
    normalized_features = Column(JSON, nullable=True)

    # Price signals
    target_price = Column(Float, nullable=True)
    max_price = Column(Float, nullable=True)

    # Demand & context
    quantity_interest = Column(Integer, default=1)
    time_horizon = Column(String, nullable=True)      # e.g. "World Cup", "Q2"
    buyer_cluster = Column(String, nullable=True)

    # Lifecycle
    status = Column(String, default="open")           # open / picked / converted
    created_at = Column(DateTime, default=datetime.utcnow)
