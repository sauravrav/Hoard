from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from models.models import get_db
from transfer_script import transfer_funds
from pydantic import BaseModel

router = APIRouter()

class TransferRequest(BaseModel):
    sender_account: int
    receiver_account: int
    amount: float

@router.post("/transfer")
async def transfer(request: TransferRequest, db: Session = Depends(get_db)):
    try:
        result = transfer_funds(
            db, 
            sender_account=request.sender_account,
            receiver_account=request.receiver_account,
            amount=request.amount
        )
        return {"message": "Transfer successful", "result": result}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
