from models.models import Account, Transaction
from models.models import SessionLocal
from sqlalchemy import exc

session = SessionLocal()

def get_account_by_user_and_type(user_id, account_type):
    account = session.query(Account).filter_by(user_id=user_id, account_type=account_type).first()
    if not account:
        raise ValueError(f"No {account_type} account found for user ID {user_id}")
    return account.id

def transfer_funds(source_account_id, target_account_id, amount):
    """Transfer funds between accounts."""
    try:
        sender_account = session.query(Account).filter_by(id=source_account_id).with_for_update().one()
        recipient_account = session.query(Account).filter_by(id=target_account_id).with_for_update().one()

        if sender_account.balance < amount:
            raise ValueError("Insufficient funds in the sender's account.")

        sender_account.balance -= amount
        recipient_account.balance += amount

        transaction = Transaction(
            source_account_id=sender_account.id,
            target_account_id=recipient_account.id,
            amount=amount,
            # description=f"Transfer from account {source_account_id} to account {target_account_id}"
        )
        session.add(transaction)

        session.commit()
        print("Transfer completed successfully.")

    except exc.SQLAlchemyError as e:
        session.rollback()
        print(f"Database error occurred: {e}")
    except Exception as e:
        session.rollback()
        print(f"An error occurred: {e}")
    finally:
        session.close()

# try:
#     user1_savings_account_id = get_account_by_user_and_type(user_id=2, account_type="savings")
#     user2_savings_account_id = get_account_by_user_and_type(user_id=1, account_type="savings")
#     transfer_funds(user1_savings_account_id, user2_savings_account_id, 3000)
# except Exception as e:
#     print(f"Error during transfer: {e}")