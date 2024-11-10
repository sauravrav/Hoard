from sqlalchemy import Column, Integer, ForeignKey
from .models import Base
from sqlalchemy.orm import relationship

class BankUser(Base):
    __tablename__ = 'bank_user'
    id = Column(Integer, primary_key=True)
    bank_id = Column(Integer, ForeignKey('banks.id'), nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    
    user = relationship("User", back_populates="bank_users")
    bank = relationship("Bank", back_populates="bank_users")