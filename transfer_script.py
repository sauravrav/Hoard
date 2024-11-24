from models.models import Account, Transaction
from models.models import SessionLocal
from sqlalchemy import exc
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError

session = SessionLocal()
def transfer_funds(source_account_id, target_account_id, amount):
    try:
        MIN_BALANCE_SAVINGS = 50
        MIN_BALANCE_CURRENT = 100

        sender_account_query = text("""
            SELECT * FROM accounts WHERE id = :source_account_id FOR UPDATE
        """)
        sender_account = session.execute(sender_account_query, {"source_account_id": source_account_id}).fetchone()

        if not sender_account:
            return "Sender's account not found."

        recipient_account_query = text("""
            SELECT * FROM accounts WHERE id = :target_account_id FOR UPDATE
        """)
        recipient_account = session.execute(recipient_account_query, {"target_account_id": target_account_id}).fetchone()

        if not recipient_account:
            return "Recipient's account not found."
        if sender_account.balance < amount:
            return "Insufficient funds in the sender's account."

        min_balance = MIN_BALANCE_SAVINGS if sender_account.account_type == "savings" else MIN_BALANCE_CURRENT

        if (sender_account.balance - amount) < min_balance:
            return f"Transfer denied. Sender must maintain a minimum balance of {min_balance}."

        update_sender_query = text("""
            UPDATE accounts SET balance = balance - :amount WHERE id = :source_account_id
        """)
        session.execute(update_sender_query, {"amount": amount, "source_account_id": source_account_id})

        update_recipient_query = text("""
            UPDATE accounts SET balance = balance + :amount WHERE id = :target_account_id
        """)
        session.execute(update_recipient_query, {"amount": amount, "target_account_id": target_account_id})

        insert_transaction_query = text("""
            INSERT INTO transactions (source_account_id, target_account_id, amount, description, timestamp)
            VALUES (:source_account_id, :target_account_id, :amount, :description, NOW())
        """)
        session.execute(insert_transaction_query, {
            "source_account_id": source_account_id,
            "target_account_id": target_account_id,
            "amount": amount,
            "description": f"Transfer of {amount} from account ID {source_account_id} to account ID {target_account_id}"
        })
        
        session.commit()
        print("Transfer completed successfully.")
        return None

    except SQLAlchemyError as e:
        session.rollback()
        return f"Database error occurred: {e}"
    except Exception as e:
        session.rollback()
        return f"An error occurred: {e}"
    finally:
        session.close()