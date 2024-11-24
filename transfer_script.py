from models.models import Account, Transaction
from models.models import SessionLocal
from sqlalchemy import exc

session = SessionLocal()

def get_account_by_user_and_type(user_id, account_type):
    account = session.query(Account).filter_by(user_id=user_id, account_type=account_type).first()
    if not account:
        raise ValueError(f"No {account_type} account found for user ID {user_id}")
    return account.id

from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError

def transfer_funds(source_account_id, target_account_id, amount):
    """Transfer funds between accounts using raw SQL."""
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
            INSERT INTO transactions (source_account_id, target_account_id, amount, description)
            VALUES (:source_account_id, :target_account_id, :amount, :description)
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

# try:
#     user1_savings_account_id = get_account_by_user_and_type(user_id=2, account_type="savings")
#     user2_savings_account_id = get_account_by_user_and_type(user_id=1, account_type="savings")
#     transfer_funds(user1_savings_account_id, user2_savings_account_id, 3000)
# except Exception as e:
#     print(f"Error during transfer: {e}")