from fastapi import APIRouter, HTTPException, Depends, Form
from sqlalchemy.orm import Session
from sqlalchemy import and_
from models.models import get_db, User, Account, Transaction, Bank, BankUser

router = APIRouter()

@router.post("/login")
def login(email: str = Form(...), password: str = Form(...), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == email).first()
    if not user or user.password != password:
        raise HTTPException(status_code=401, detail="Invalid email or password")

    savings_account = db.query(Account).filter(
        and_(Account.user_id == user.id, Account.account_type == "savings")
    ).first()
    savings_balance = savings_account.balance if savings_account else 0

    recent_transactions = db.query(Transaction).filter(
        (Transaction.source_account_id == savings_account.id) | 
        (Transaction.target_account_id == savings_account.id)
    ).order_by(Transaction.timestamp.desc()).limit(5).all()
    transactions_data = [
        {
            "id": transaction.id,
            "type": "credit" if transaction.target_account_id == savings_account.id else "debit",
            "amount": transaction.amount,
            "timestamp": transaction.timestamp
        } for transaction in recent_transactions
    ]

    associated_banks = db.query(Bank).join(BankUser).filter(BankUser.user_id == user.id).all()
    banks_data = [{"id": bank.id, "name": bank.name, "location": bank.location} for bank in associated_banks]

    return {
        "message": "Login successful!",
        "token": user.email,
        "user": {
            "name": f"{user.first_name} {user.last_name}",
            "email": user.email,
            "savings_balance": savings_balance,
            "recent_transactions": transactions_data,
            "banks": banks_data,
        }
    }