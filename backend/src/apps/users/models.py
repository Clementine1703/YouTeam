from config.database import Base
from sqlalchemy import Column, String, Integer, Boolean, ForeignKey
from sqlalchemy.orm import relationship


class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(length=50), unique=True)
    email = Column(String(length=100))
    full_name = Column(String(length=50))
    hashed_password = Column(String)
    disabled = Column(Boolean())

    role_id = Column(Integer, ForeignKey('role.id'), nullable=True)
    role = relationship("Role", back_populates="user")