import threading
import time
from sqlalchemy import text
from models.models import get_session

class Simulate_Isolation:
    def transfer_funds_isolation(self, source_account_id, target_account_id, amount, isolation_level="SERIALIZABLE"):
        session = get_session(isolation_level=isolation_level)
        try:
            MIN_BALANCE = 1000
            sender_query = text("SELECT * FROM accounts WHERE id = :source_account_id FOR UPDATE")
            recipient_query = text("SELECT * FROM accounts WHERE id = :target_account_id FOR UPDATE")
            
            sender_account = session.execute(sender_query, {"source_account_id": source_account_id}).fetchone()
            if not sender_account:
                return "Sender account not found."

            recipient_account = session.execute(recipient_query, {"target_account_id": target_account_id}).fetchone()
            if not recipient_account:
                return "Recipient account not found."

            print(f"Transaction 1: Sender balance before transfer: {sender_account.balance}")
            print(f"Transaction 1: Recipient balance before transfer: {recipient_account.balance}")

            if sender_account.balance < amount:
                return "Insufficient funds."
            if sender_account.balance - amount < MIN_BALANCE:
                return f"Minimum balance of ${MIN_BALANCE} must be maintained."

            time.sleep(5)
            update_sender = text("UPDATE accounts SET balance = balance - :amount WHERE id = :source_account_id")
            update_recipient = text("UPDATE accounts SET balance = balance + :amount WHERE id = :target_account_id")

            session.execute(update_sender, {"amount": amount, "source_account_id": source_account_id})
            session.execute(update_recipient, {"amount": amount, "target_account_id": target_account_id})
            session.commit()

            print("Transaction 1: Committed successfully")
            return None
        except Exception as e:
            session.rollback()
            return f"Error: {str(e)}"
        finally:
            session.close()

    def simulate_concurrency(self, amount: float, isolation_level="SERIALIZABLE"):
        def transaction1():
            result = self.transfer_funds_isolation(1, 2, amount, isolation_level=isolation_level)
            print("Transaction 1:", result or "Committed successfully")

        def transaction2():
            time.sleep(3)
            session = get_session(isolation_level=isolation_level)
            try:
                print("Transaction 2: Starting")
                sender_query = text("SELECT * FROM accounts WHERE id = :id")
                sender = session.execute(sender_query, {"id": 1}).fetchone()
                recipient = session.execute(sender_query, {"id": 2}).fetchone()

                print(
                    f"Transaction 2 (During Transaction 1) - Account 1 Balance: {sender.balance}, Account 2 Balance: {recipient.balance}"
                )
            except Exception as e:
                print(f"Transaction 2 error: {e}")
            finally:
                session.close()
        
        def print_final_balances():
            session = get_session()
            try:
                sender_query = text("SELECT * FROM accounts WHERE id = :id")
                sender = session.execute(sender_query, {"id": 1}).fetchone()
                recipient = session.execute(sender_query, {"id": 2}).fetchone()

                print(
                    f"After Commit - Account 1 Balance: {sender.balance}, Account 2 Balance: {recipient.balance}"
                )
            except Exception as e:
                print(f"Final balance query error: {e}")
            finally:
                session.close()

        t1 = threading.Thread(target=transaction1)
        t2 = threading.Thread(target=transaction2)
        t1.start()
        time.sleep(2)
        t2.start()
        t1.join()
        t2.join()
        print_final_balances()
        
if __name__ == "__main__":
    isolation_simulator = Simulate_Isolation()
    print("Isolation-problem-4")
    isolation_simulator.simulate_concurrency(500, isolation_level="SERIALIZABLE")
    '''
    print("Starting transfer with sufficient balance and maintaining minimum balance (READ_COMMITTED)")
    isolation_simulator.simulate_concurrency(500, isolation_level="READ_COMMITTED")

    print("2a")
    # Fails due to insufficient balance constraint
    isolation_simulator.simulate_concurrency(3000, isolation_level="READ_COMMITTED") 

    print("2b")
    # Fails due to minimum balance constraint
    isolation_simulator.simulate_concurrency(1500, isolation_level="READ_COMMITTED") 
    '''