from fastapi import APIRouter, HTTPException, Depends, Form
from pydantic import BaseModel
from sqlalchemy import text
from sqlalchemy.orm import Session
from models.models import get_db, Customer, Order

router = APIRouter()
class AddressUpdate(BaseModel):
    new_address: str

@router.put("/customer/{customer_id}/address")
def update_address(customer_id: int, address: AddressUpdate, db: Session = Depends(get_db)):
    try:
        new_address = address.new_address
        check_customer_query = text("""
            SELECT * FROM customers WHERE id = :customer_id
        """)
        customer = db.execute(check_customer_query, {"customer_id": customer_id}).fetchone()
        if not customer:
            raise HTTPException(status_code=404, detail="Customer not found")
        update_customer_query = text("""
            UPDATE customers SET address = :new_address WHERE id = :customer_id
        """)
        db.execute(update_customer_query, {"new_address": new_address, "customer_id": customer_id})
        update_order_query = text("""
            UPDATE orders SET shipping_address = :new_address WHERE customer_id = :customer_id
        """)
        db.execute(update_order_query, {"new_address": new_address, "customer_id": customer_id})
        db.commit()
        return {"message": "Address updated successfully"}
    
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")

@router.post("/login")
def login(email: str = Form(...), password: str = Form(...), db: Session = Depends(get_db)):
    try:
        login_query = text("""
            SELECT * FROM customers WHERE email = :email
        """)
        user = db.execute(login_query, {"email": email}).fetchone()

        if not user or user.encrypted_password != password:
            raise HTTPException(status_code=401, detail="Invalid email or password")

        return {
            "message": "Login successful!",
            "token": user.email,
            "password": user.encrypted_password,
            "address": user.address,
            "customer_id": user.id
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")