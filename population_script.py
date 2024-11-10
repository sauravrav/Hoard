from sqlalchemy.orm import Session
from models.models import Bank, User, Account, Transaction, BankUser
from models.models import SessionLocal

session = SessionLocal()

try:
    bank1 = Bank(name="Chase Bank")
    bank2 = Bank(name="Wells Fargo Bank")
    session.add_all([bank1, bank2])
    
    user1 = User(first_name="Ali", last_name="Khalilabadi", email="ali@sfbu", role="customer")
    user2 = User(first_name="Niyan", last_name="Danny", email="niyan@danny", role="customer")
    session.add_all([user1, user2])

    session.commit()

    account11 = Account(account_type="savings", user_id=user1.id, bank_id=bank1.id, balance=1000)
    account12 = Account(account_type="current", user_id=user1.id, bank_id=bank1.id, balance=500)
    
    account21 = Account(account_type="savings", user_id=user2.id, bank_id=bank2.id, balance=2000)
    account22 = Account(account_type="current", user_id=user2.id, bank_id=bank2.id, balance=100)
    
    session.add_all([account11, account12, account21, account22])

    bank_user1 = BankUser(bank_id=bank1.id, user_id=user1.id)
    bank_user2 = BankUser(bank_id=bank2.id, user_id=user2.id)
    session.add_all([bank_user1, bank_user2])
    
    session.commit()
    print("Data populated successfully.")

except Exception as e:
    session.rollback()
    print(f"Error: {e}")
finally:
    session.close()
