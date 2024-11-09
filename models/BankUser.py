from sqlalchemy import Column, Integer, ForeignKey
from .models import Base

class BankUser(Base):
    __tablename__ = 'bank_user'
    id = Column(Integer, primary_key=True)
    bank_id = Column(Integer, ForeignKey('banks.id'), nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    account_id = Column(Integer, ForeignKey('accounts.id'), nullable=False)