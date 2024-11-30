import time
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import text
from sqlalchemy.orm import Session
from models.models import get_db
from transfer_script import transfer_funds
from pydantic import BaseModel
import threading

router = APIRouter()

class TransferRequest(BaseModel):
    sender_account: int
    receiver_account: int
    amount: float

@router.post("/transfer")
async def transfer(request: TransferRequest, db: Session = Depends(get_db)):
    try:
        error_message = transfer_funds(
            source_account_id=request.sender_account,
            target_account_id=request.receiver_account,
            amount=request.amount,
        )
        if error_message:
            raise HTTPException(status_code=400, detail=error_message)
        
        return {"message": "Transfer successful"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/simulate-concurrency")
def simulate_concurrency(amount: float, db: Session = Depends(get_db)):
    def transaction1():
        result = transfer_funds(1, 2, amount, isolation_level="READ_COMMITTED")
        print("Transaction 1:", result or "Committed successfully")
    
    def transaction2():
        session = db()
        try:
            sender_query = text("SELECT * FROM accounts WHERE id = :id")
            sender = session.execute(sender_query, {"id": 1}).fetchone()
            recipient = session.execute(sender_query, {"id": 2}).fetchone()
            print(f"Transaction 2 - Account 1 Balance: {sender.balance}, Account 2 Balance: {recipient.balance}")
        finally:
            session.close()

    t1 = threading.Thread(target=transaction1)
    t2 = threading.Thread(target=transaction2)
    t1.start()
    time.sleep(2)
    t2.start()
    t1.join()
    t2.join()
