from sqlalchemy import Column, Integer, Float, String, JSON, DateTime
from datetime import datetime
from db import Base

class ValueInsight(Base):
    __tablename__ = "value_insights"

    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, nullable=False)
    buyer_id = Column(Integer, nullable=False)

    value_score = Column(Float)
    plateau = Column(String)
    differentiation = Column(Float)
    elasticity = Column(Float)
    elasticity_label = Column(String)
    recommended_price = Column(Float)
    raw_answers = Column(JSON)

    created_at = Column(DateTime, default=datetime.utcnow)
