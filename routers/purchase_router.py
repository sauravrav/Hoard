import logging
from typing import Optional
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from models.models import get_db, Product, Customer, Order
from pydantic import BaseModel
from sqlalchemy import text

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

router = APIRouter()
class PurchaseRequest(BaseModel):
    customer_id: int
    product_id: int
    quantity: int
    new_address: Optional[str] = None

@router.post("/purchase")
def purchase_product(request: PurchaseRequest, db: Session = Depends(get_db)):
    try:
        with db.begin_nested():
            customer_query = text("SELECT * FROM customers WHERE id = :customer_id")
            customer = db.execute(customer_query, {"customer_id": request.customer_id}).fetchone()
            
            if not customer:
                raise HTTPException(status_code=400, detail=f"Invalid customer ID: {request.customer_id}")

            product_query = text("SELECT * FROM products WHERE id = :product_id")
            product = db.execute(product_query, {"product_id": request.product_id}).fetchone()

            if not product:
                raise HTTPException(status_code=400, detail=f"Invalid product ID: {request.product_id}")

            if request.new_address and customer.address != request.new_address:
                update_address_query = text("""
                    UPDATE customers SET address = :new_address WHERE id = :customer_id
                """)
                db.execute(update_address_query, {"new_address": request.new_address, "customer_id": request.customer_id})

                update_orders_query = text("""
                    UPDATE orders SET shipping_address = :new_address WHERE customer_id = :customer_id
                """)
                db.execute(update_orders_query, {"new_address": request.new_address, "customer_id": request.customer_id})

            if product.quantity < request.quantity:
                raise HTTPException(status_code=400, detail="Insufficient product quantity")

            update_product_query = text("""
                UPDATE products SET quantity = quantity - :quantity WHERE id = :product_id
            """)
            db.execute(update_product_query, {"quantity": request.quantity, "product_id": request.product_id})

            insert_order_query = text("""
                INSERT INTO orders (product_id, customer_id, quantity, shipping_address)
                VALUES (:product_id, :customer_id, :quantity, :shipping_address)
            """)
            db.execute(insert_order_query, {
                "product_id": request.product_id,
                "customer_id": request.customer_id,
                "quantity": request.quantity,
                "shipping_address": request.new_address or customer.address,
            })

            db.commit()

        return {"message": "Purchase successful"}

    except Exception as e:
        db.rollback()
        logger.error(f"Error during purchase: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")