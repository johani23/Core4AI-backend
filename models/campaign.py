from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.sql import func
from db import Base


class Campaign(Base):
    __tablename__ = "campaigns"

    id = Column(Integer, primary_key=True, index=True)

    # -------------------------------------------------
    # Relations (ONE of them must exist)
    # -------------------------------------------------
    product_id = Column(
        Integer,
        ForeignKey("products.id"),
        nullable=True
    )

    intention_id = Column(
        Integer,
        nullable=True
    )

    # -------------------------------------------------
    # Campaign execution data
    # -------------------------------------------------
    audience = Column(String(100), nullable=False)
    influencer = Column(String(100), nullable=False)

    recommended_price = Column(Float, nullable=True)
    ai_success_score = Column(Float, nullable=True)

    status = Column(String(50), default="نشطة")

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )
