from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from db.database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    coins = Column(Integer, default=100)
    xp = Column(Integer, default=0)
    badge = Column(String, default="Newbie")
    cluster_id = Column(Integer, ForeignKey("clusters.id"))
    cluster = relationship("Cluster", back_populates="members")

class Cluster(Base):
    __tablename__ = "clusters"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True)
    members = relationship("User", back_populates="cluster")

class Duel(Base):
    __tablename__ = "duels"
    id = Column(Integer, primary_key=True, index=True)
    challenger_id = Column(Integer, ForeignKey("users.id"))
    opponent_id = Column(Integer, ForeignKey("users.id"))
    winner_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class Transaction(Base):
    __tablename__ = "transactions"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    amount = Column(Integer)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class Journey(Base):
    __tablename__ = "journeys"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    from_cluster = Column(String)
    to_cluster = Column(String)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())

class RecommendationLog(Base):
    __tablename__ = "recommendation_logs"
    id = Column(Integer, primary_key=True, index=True)
    cluster = Column(String, index=True)
    suggestion_type = Column(String)
    forecast_state = Column(String)
    executed = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    executed_at = Column(DateTime(timezone=True), nullable=True)

class Post(Base):
    __tablename__ = "posts"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    cluster_id = Column(Integer, ForeignKey("clusters.id"))
    content = Column(Text)
    upvotes = Column(Integer, default=0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
