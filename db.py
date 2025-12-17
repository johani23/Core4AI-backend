# ============================================================================
# 💚 Core4.AI – Database Engine / Session (SQLite + SQLAlchemy)
# ============================================================================

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# SQLite database
SQLALCHEMY_DATABASE_URL = "sqlite:////data/core4.db"


engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False}  # SQLite required option
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


# Dependency: DB session generator
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
