from src.config.database import Base
from sqlalchemy import Column, String, Integer


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(length=50))
    mail = Column(String(length=100))