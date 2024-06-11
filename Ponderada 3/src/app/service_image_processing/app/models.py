from sqlalchemy import Column, Integer, String, create_engine, Sequence
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

class Image(Base):
    __tablename__ = 'images'
    id = Column(Integer, Sequence('image_id_seq'), primary_key=True)
    filename = Column(String(100))
    status = Column(String(50))

# Database setup
DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base.metadata.create_all(bind=engine)
