from fastapi import APIRouter, HTTPException, Depends, Form
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

@router.post("/login")
def login(email: str = Form(...), password: str = Form(...), db: Session = Depends(get_db)):
    user = db.query(Customer).filter(Customer.email == email).first()
    if not user or user.password != password:
        raise HTTPException(status_code=401, detail="Invalid email or password")
    return {
        "message": "Login successful!",
        "token": user.email,
        "password": user.password
    }