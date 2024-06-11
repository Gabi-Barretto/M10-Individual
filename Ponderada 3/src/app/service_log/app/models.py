from sqlalchemy import Column, Integer, String, create_engine, Sequence
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

class Log(Base):
    __tablename__ = 'logs'
    id = Column(Integer, Sequence('log_id_seq'), primary_key=True)
    action = Column(String(50))
    user_id = Column(Integer)

# Database setup
DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base.metadata.create_all(bind=engine)
