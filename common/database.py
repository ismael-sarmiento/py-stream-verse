from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

DATABASE_URL_POSTGRES = "postgresql+psycopg2://user:pass@db:5432/audiovisual"
DATABASE_URL_SQLITE = "sqlite:////Users/isarmiento/Personal/ISarmiento/Projects/py-stream-verse/test.db"

engine = create_engine(DATABASE_URL_SQLITE, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
