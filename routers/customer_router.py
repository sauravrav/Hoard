
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from models.models import get_db, Customer, Order

router = APIRouter()
@router.put("/customer/{customer_id}/address")
def update_address(customer_id: int, new_address: str, db: Session = Depends(get_db)):
    customer = db.query(Customer).filter(Customer.id == customer_id).first()
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")

    customer.address = new_address

    db.query(Order).filter(Order.customer_id == customer_id).update({"shipping_address": new_address})

    db.commit()
    return {"message": "Address updated successfully"}