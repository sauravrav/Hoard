from sqlalchemy import text
from models.models import SessionLocal
from models.Product_Customer_Order import Product, Customer, Order

def display_table(session, table_name):
    print(f"\nContents of {table_name.title()} Table:")
    rows = session.execute(text(f"SELECT * FROM {table_name}")).fetchall()
    if rows:
        for row in rows:
            print(row)
    else:
        print(f"{table_name.title()} table is empty.")

def handle_transaction(session, customer_id, product_id, quantity, address, simulate_error=False):
    try:
        print("\nStarting a new transaction...")
        customer = session.execute(
            text(f"SELECT * FROM customers WHERE id = {customer_id}")
        ).fetchone()
        if customer:
            current_address = customer.address
            if current_address != address:
                print(f"Updating customer's address from '{current_address}' to '{address}'...")
                session.execute(
                    text(
                        f"UPDATE customers SET address = :new_address WHERE id = :customer_id"
                    ),
                    {"new_address": address, "customer_id": customer_id},
                )
        new_order = Order(
            customer_id=customer_id,
            product_id=product_id,
            quantity=quantity,
            shipping_address=address,
        )
        session.add(new_order)
        if simulate_error:
            raise Exception("Simulated exception during transaction!")

        session.commit()
        print("Transaction committed successfully!")
    except Exception as e:
        session.rollback()
        print(f"Transaction failed and rolled back: {e}")
    finally:
        display_table(session, "orders")
def simulate_durability():
    session = SessionLocal()
    try:
        display_table(session, "orders")
        print("\n--- Case 1: Successful Transaction ---")
        customer_id = 3
        product_id = 2
        customer_query = text(f"SELECT * FROM customers WHERE id = {customer_id}")
        product_query = text(f"SELECT * FROM products WHERE id = {product_id}")
        customer = session.execute(customer_query).fetchone()
        product = session.execute(product_query).fetchone()
        if customer and product:
            handle_transaction(
                session,
                customer_id=customer.id,
                product_id=product.id,
                quantity=2,
                address="Kasol, Himachal",
                simulate_error=False,
            )
        print("\n--- Case 2: Failed Transaction ---")
        if customer and product:
            handle_transaction(
                session,
                customer_id=customer.id,
                product_id=product.id,
                quantity=1,
                address="Leh, Ladakh",
                simulate_error=True,
            )
    finally:
        session.close()
if __name__ == "__main__":
    simulate_durability()