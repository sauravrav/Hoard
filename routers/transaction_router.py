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
