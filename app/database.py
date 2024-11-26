# # database.py
# from sqlalchemy import create_engine
# from sqlalchemy.orm import sessionmaker, declarative_base

# DATABASE_URL = "postgresql://postgres:sourabh%402175@localhost:5432/fastapidatabase"  # Replace with your database URL
# engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})  # SQLite-specific args
# SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
# Base = declarative_base()

# # Dependency to get DB session
# def get_db():
#     db = SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Replace with your PostgreSQL connection details
DATABASE_URL = "postgresql://postgres:sourabh%402175@localhost:5432/fastapidatabase"

# Create the SQLAlchemy engine for PostgreSQL
engine = create_engine(DATABASE_URL)

# Configure the sessionmaker
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Declare a base for the models
Base = declarative_base()

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

