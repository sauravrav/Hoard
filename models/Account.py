from sqlalchemy import Column, Integer, String, ForeignKey
from .models import Base
from sqlalchemy.orm import relationship

class Account(Base):
    __tablename__ = 'accounts'
    id = Column(Integer, primary_key=True)
    account_type = Column(String, nullable=False)
    balance = Column(Integer, default=0)
    bank_id = Column(Integer, ForeignKey('banks.id'), nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)

    bank = relationship("Bank", back_populates="accounts")
    user = relationship("User", back_populates="accounts")
