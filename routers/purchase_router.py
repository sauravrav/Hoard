import logging
from typing import Optional
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from models.models import get_db, Product, Customer, Order
from pydantic import BaseModel

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
            customer = db.query(Customer).filter(Customer.id == request.customer_id).first()
            product = db.query(Product).filter(Product.id == request.product_id).first()

            if not customer:
                logger.error(f"Invalid customer ID: {request.customer_id}")
                raise HTTPException(status_code=400, detail=f"Invalid customer ID: {request.customer_id}")
            if not product:
                logger.error(f"Invalid product ID: {request.product_id}")
                raise HTTPException(status_code=400, detail=f"Invalid product ID: {request.product_id}")

            if request.new_address and customer.address != request.new_address:
                customer.address = request.new_address
                db.query(Order).filter(Order.customer_id == request.customer_id).update({"shipping_address": request.new_address})
                logger.info(f"Updated address for customer {request.customer_id}")

            if product.quantity < request.quantity:
                logger.warning(f"Insufficient product quantity for product_id {request.product_id}. Requested: {request.quantity}, Available: {product.quantity}")
                raise HTTPException(status_code=400, detail="Insufficient product quantity")

            product.quantity -= request.quantity
            logger.info(f"Product quantity updated for product_id {request.product_id}: Remaining {product.quantity}")

            new_order = Order(
                product_id=request.product_id,
                customer_id=request.customer_id,
                quantity=request.quantity,
                shipping_address=request.new_address or customer.address
            )
            db.add(new_order)
            logger.info(f"Order created: {new_order}")

            db.commit()

        return {"message": "Purchase successful"}

    except Exception as e:
        db.rollback()
        logger.error(f"Error during purchase: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")