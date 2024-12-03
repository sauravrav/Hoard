from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

Base = declarative_base()

DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)

def get_session(isolation_level="SERIALIZABLE"):
    connection = engine.connect()
    connection = connection.execution_options(isolation_level=isolation_level)
    Session = sessionmaker(bind=connection, autocommit=False)
    return Session()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

from models.User import User
from models.Account import Account
from models.BankUser import BankUser
from models.Bank import Bank
from models.Transaction import Transaction
from models.Product_Customer_Order import Product, Customer, Order