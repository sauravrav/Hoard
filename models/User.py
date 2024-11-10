from sqlalchemy import Column, Integer, String
from .models import Base
from sqlalchemy.orm import relationship

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    first_name = Column(String)
    last_name = Column(String)
    email = Column(String, unique=True)
    role = Column(String)
    
    accounts = relationship("Account", back_populates="user")
    bank_users = relationship("BankUser", back_populates="user")