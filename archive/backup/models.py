from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import declarative_base, relationship
from datetime import datetime

Base = declarative_base()

class Creator(Base):
    __tablename__ = "creators"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    tribe_id = Column(Integer, ForeignKey("tribes.id"))
    level = Column(String, default="Rising Voice")
    tribe = relationship("Tribe", back_populates="members")

class Tribe(Base):
    __tablename__ = "tribes"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    avg_mastery = Column(Float, default=0.0)
    members = relationship("Creator", back_populates="tribe")

class Upload(Base):
    __tablename__ = "uploads"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    tribe_id = Column(Integer)
    filename = Column(String)
    timestamp = Column(DateTime, default=datetime.utcnow)

class MasteryScore(Base):
    __tablename__ = "mastery_scores"
    id = Column(Integer, primary_key=True)
    creator_name = Column(String)
    upload_id = Column(Integer)
    score = Column(Integer)
    level = Column(String)
