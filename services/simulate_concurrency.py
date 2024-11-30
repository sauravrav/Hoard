
import threading
import time
from sqlalchemy import text
from transfer_script import transfer_funds_isolation
from models.models import SessionLocal


def simulate_concurrency(amount: float):
    def transaction1():
        result = transfer_funds_isolation(1, 2, amount, isolation_level="READ_COMMITTED")
        print("Transaction 1:", result or "Committed successfully")
    
    def transaction2():
        session = SessionLocal()
        try:
            sender_query = text("SELECT * FROM accounts WHERE id = :id")
            sender = session.execute(sender_query, {"id": 1}).fetchone()
            recipient = session.execute(sender_query, {"id": 2}).fetchone()
            print(f"Transaction 2 - Account 1 Balance: {sender.balance}, Account 2 Balance: {recipient.balance}")
        finally:
            session.close()

    t1 = threading.Thread(target=transaction1)
    t2 = threading.Thread(target=transaction2)
    t1.start()
    time.sleep(2)
    t2.start()
    t1.join()
    t2.join()