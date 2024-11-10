from sqlalchemy import Column, Integer, ForeignKey, DateTime, String
from .models import Base
from sqlalchemy.orm import relationship
from datetime import datetime, timezone

class Transaction(Base):
    __tablename__ = 'transactions'
    id = Column(Integer, primary_key=True)
    source_account_id = Column(Integer, ForeignKey('accounts.id'), nullable=False)
    target_account_id = Column(Integer, ForeignKey('accounts.id'), nullable=False)
    amount = Column(Integer, nullable=False)
    description = Column(String, nullable=True)
    timestamp = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    source_account = relationship("Account", foreign_keys=[source_account_id])
    target_account = relationship("Account", foreign_keys=[target_account_id])