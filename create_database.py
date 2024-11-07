import os
from dotenv import load_dotenv # type: ignore
from sqlalchemy import create_engine # type: ignore

load_dotenv()

DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_HOST = os.getenv('DB_HOST')
DB_PORT = os.getenv('DB_PORT', '5432')

DATABASE_URL = f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/postgres"

engine = create_engine(DATABASE_URL)

with engine.connect() as connection:
    connection.execute("commit")
    connection.execute("CREATE DATABASE your_database_name")