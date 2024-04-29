from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .models import Base  # Verifique se este import está correto

DATABASE_URL = "sqlite:///./test.db"  # Ajuste o caminho conforme necessário

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def create_db():
    Base.metadata.create_all(bind=engine)
