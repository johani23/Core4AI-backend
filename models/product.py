from sqlalchemy import Column, Integer, String, Float, Text
from db import Base


class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)

    # -------------------------
    # Core product identity
    # -------------------------
    name = Column(String(255), nullable=False)
    category = Column(String(100), nullable=True)
    description = Column(Text, nullable=True)

    # -------------------------
    # Pricing (CRITICAL)
    # -------------------------
    price = Column(Float, nullable=False)
    competitor_price = Column(
        Float,
        nullable=False,
        default=0.0
    )

    # -------------------------
    # Feature intelligence
    # Stored as JSON string
    # -------------------------
    features = Column(
        Text,
        nullable=False,
        default="[]"
    )

    # -------------------------
    # Media
    # -------------------------
    image_url = Column(String(500), nullable=True)
