from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Database URL (SQLite for now)
# URL format: <dialect>+<driver>://<username>:<password>@<host>:<port>/<database>
SQLALCHEMY_DATABASE_URL = "sqlite:///backend/app.db"

engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}, echo=True)

SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)

Base = declarative_base()