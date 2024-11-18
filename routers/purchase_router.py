from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from models.models import get_db, Product, Customer, Order

router = APIRouter()

@router.post("/purchase")
def purchase_product(customer_id: int, product_id: int, quantity: int, new_address: str, db: Session = Depends(get_db)):
    customer = db.query(Customer).filter(Customer.id == customer_id).first()
    product = db.query(Product).filter(Product.id == product_id).first()

    if not customer:
        raise HTTPException(status_code=400, detail="Invalid customer ID")
    if not product:
        raise HTTPException(status_code=400, detail="Invalid product ID")

    if not new_address:
        raise HTTPException(status_code=400, detail="Address update required for consistency")
    customer.address = new_address
    db.commit()

    if product.quantity < quantity:
        raise HTTPException(status_code=400, detail="Insufficient product quantity")
    elif product.quantity == 0:
        raise HTTPException(status_code=400, detail="Product out of stock")
    else:
        product.quantity -= quantity
        new_order = Order(product_id=product_id, customer_id=customer_id, quantity=quantity)
        db.add(new_order)
        db.commit()

    return {"message": "Purchase successful"}
