import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, text

load_dotenv()

DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_HOST = os.getenv('DB_HOST')
DB_PORT = os.getenv('DB_PORT', '5432')
DB_NAME = "bank_system"

DATABASE_URL = f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/postgres"

engine = create_engine(DATABASE_URL, isolation_level="AUTOCOMMIT")

with engine.connect() as connection:
    connection.execute(text(f"CREATE DATABASE {DB_NAME}"))

print(f"Succesfully created the database {DB_NAME}")