from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    pedido = Column(String)

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "pedido": self.pedido
        }
