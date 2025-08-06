from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# MySQL Connection URL Format:
# mysql+pymysql://<username>:<password>@<host>/<database>
DATABASE_URL = "mysql+pymysql://root:@localhost:3306/edtech_db"

engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
    echo=True  # Shows SQL logs in console for debugging
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
