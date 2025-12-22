# ============================================================================
# 🛡 TribeSignal Model — Economic Trust Unit
# ============================================================================

from sqlalchemy import Column, String, Float, Boolean, DateTime
from sqlalchemy.sql import func
from db import Base


class TribeSignal(Base):
    __tablename__ = "tribe_signals"

    id = Column(String, primary_key=True)
    tribe_id = Column(String, index=True)
    product_id = Column(String, index=True)

    context_fit_score = Column(Float)
    regret_risk = Column(Float)
    value_per_year = Column(String)  # low | medium | high
    integrity_flag = Column(Boolean, default=False)
    eligibility_state = Column(String)  # trusted | neutral | flagged

    evaluated_at = Column(DateTime, default=func.now())
