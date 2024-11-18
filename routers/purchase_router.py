import logging
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from models.models import get_db, Product, Customer, Order

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

router = APIRouter()

@router.post("/purchase")
def purchase_product(customer_id: int, product_id: int, quantity: int, new_address: str = None, db: Session = Depends(get_db)):
    try:
        with db.begin_nested():
            customer = db.query(Customer).filter(Customer.id == customer_id).first()
            product = db.query(Product).filter(Product.id == product_id).first()

            if not customer:
                logger.error(f"Invalid customer ID: {customer_id}")
                raise HTTPException(status_code=400, detail="Invalid customer ID")
            if not product:
                logger.error(f"Invalid product ID: {product_id}")
                raise HTTPException(status_code=400, detail="Invalid product ID")
            
            if new_address and customer.address != new_address:
                customer.address = new_address
                db.query(Order).filter(Order.customer_id == customer_id).update({"shipping_address": new_address})
                logger.info(f"Customer address updated for customer_id: {customer_id} to {new_address}")

            if product.quantity < quantity:
                logger.warning(f"Insufficient product quantity for product_id: {product_id}. Requested: {quantity}, Available: {product.quantity}")
                raise HTTPException(status_code=400, detail="Insufficient product quantity")
            elif product.quantity == 0:
                logger.warning(f"Product out of stock for product_id: {product_id}")
                raise HTTPException(status_code=400, detail="Product out of stock")
            else:
                product.quantity -= quantity
                new_order = Order(product_id=product_id, customer_id=customer_id, quantity=quantity)
                db.add(new_order)
                logger.info(f"New order created for customer_id: {customer_id}, product_id: {product_id}, quantity: {quantity}")

            db.commit()

        return {"message": "Purchase successful"}

    except Exception as e:
        db.rollback()
        logger.error(f"Error processing purchase for customer_id: {customer_id}, product_id: {product_id}. Error: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")