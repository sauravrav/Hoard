from fastapi import APIRouter, HTTPException, Depends, Form
from sqlalchemy.orm import Session
from sqlalchemy import text
from models.models import get_db

router = APIRouter()

@router.post("/login")
def login(email: str = Form(...), password: str = Form(...), db: Session = Depends(get_db)):
    try:
        user_query = text("SELECT * FROM users WHERE email = :email")
        user = db.execute(user_query, {"email": email}).fetchone()

        if not user:
            raise HTTPException(status_code=401, detail="Invalid email or password")

        user_dict = dict(user._mapping)

        if user_dict["password"] != password:
            raise HTTPException(status_code=401, detail="Invalid email or password")

        accounts_query = text("""
            SELECT id 
            FROM accounts 
            WHERE user_id = :user_id
        """)
        user_accounts = db.execute(accounts_query, {"user_id": user_dict["id"]}).fetchall()
        account_ids = [account[0] for account in user_accounts]

        if not account_ids:
            return {
                "message": "Login successful!",
                "token": user_dict["email"],
                "user": {
                    "name": f"{user_dict['first_name']} {user_dict['last_name']}",
                    "email": user_dict["email"],
                    "recent_transactions": [],
                    "banks": []
                }
            }

        transactions_query = text(f"""
            SELECT id, 
                   CASE 
                       WHEN target_account_id IN :account_ids THEN 'credit' 
                       ELSE 'debit' 
                   END AS type, 
                   amount, 
                   timestamp 
            FROM transactions 
            WHERE source_account_id IN :account_ids OR target_account_id IN :account_ids
            ORDER BY timestamp DESC
            LIMIT 5
        """)
        recent_transactions = db.execute(transactions_query, {"account_ids": tuple(account_ids)}).fetchall()
        breakpoint()
        
        transactions_data = [
            {
                "id": transaction[0],
                "type": transaction[1],
                "amount": transaction[2],
                "timestamp": transaction[3]
            }
            for transaction in recent_transactions
        ]

        banks_query = text("""
            SELECT b.id AS bank_id, 
                   b.name AS bank_name, 
                   b.location, 
                   a.id AS account_id, 
                   a.account_type, 
                   a.balance
            FROM banks b
            JOIN accounts a ON b.id = a.bank_id
            WHERE a.user_id = :user_id
        """)
        bank_accounts = db.execute(banks_query, {"user_id": user_dict["id"]}).fetchall()

        banks_data = [
            {
                "bank_id": bank[0],
                "bank_name": bank[1],
                "location": bank[2],
                "account_id": bank[3],
                "account_type": bank[4],
                "balance": bank[5]
            }
            for bank in bank_accounts
        ]

        return {
            "message": "Login successful!",
            "token": user_dict["email"],
            "password": user_dict["password"],
            "user": {
                "name": f"{user_dict['first_name']} {user_dict['last_name']}",
                "email": user_dict["email"],
                "recent_transactions": transactions_data,
                "banks": banks_data,
            }
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))