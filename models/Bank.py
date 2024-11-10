from sqlalchemy import Column, Integer, String
from .models import Base
from sqlalchemy.orm import relationship

class Bank(Base):
    __tablename__ = 'banks'
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)
    location = Column(String)
    
    accounts = relationship("Account", back_populates="bank")
    bank_users = relationship("BankUser", back_populates="bank")