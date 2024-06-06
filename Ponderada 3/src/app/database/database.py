from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from app.models import user  # Certifique-se de que todos os modelos estão importados

DATABASE_URL = "sqlite:///./test.db"  # Ajuste o caminho conforme necessário

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def create_db():
    Base.metadata.create_all(bind=engine)

# Dependency for database sessions
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
