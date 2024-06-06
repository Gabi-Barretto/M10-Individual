from sqlalchemy.orm import Session
from database.models import User

class UserRepository:

    def __init__(self, db: Session):
        self.db = db

    def create_user(self, name: str, email: str, password: str):
        user = User(name=name, email=email, password=password)
        self.db.add(user)
        self.db.commit()
        return user

    def get_user_by_email(self, email: str):
        return self.db.query(User).filter(User.email == email).first()

    def get_user(self, user_id: int):
        return self.db.query(User).filter(User.id == user_id).first()

    def get_users(self):
        return self.db.query(User).all()

    def update_user(self, user_id: int, name: str, email: str, password: str):
        user = self.get_user(user_id)
        if user:
            user.name = name
            user.email = email
            user.password = password
            self.db.commit()
        return user

    def delete_user(self, user_id: int):
        user = self.get_user(user_id)
        if user:
            self.db.delete(user)
            self.db.commit()
        return user
