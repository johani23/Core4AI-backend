# ============================================================================
# 💚 Core4.AI – ProductPricingMIT Model
# ============================================================================

from sqlalchemy import Column, Integer, Float, String, DateTime
from sqlalchemy.sql import func
from db import Base

class ProductPricingMIT(Base):
    __tablename__ = "product_pricing_mit"

    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, index=True, nullable=False)

    base_price = Column(Float, nullable=False)
    competitor_price = Column(Float, nullable=False)

    smart_price = Column(Float, nullable=False)
    market_floor = Column(Float, nullable=False)
    market_ceiling = Column(Float, nullable=False)

    tribe_hotness = Column(String(100))
    conversion_lift = Column(String(20))

    created_at = Column(DateTime(timezone=True), server_default=func.now())
