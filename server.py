import socket
import psycopg2 # type: ignore
from dotenv import load_dotenv # type: ignore
from sqlalchemy.orm import sessionmaker # type: ignore
from models.models import User, engine
import os

load_dotenv()

HOST = '127.0.0.1'
PORT = 8080

# TCP socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))
server_socket.listen(5)
print(f"Serving HTTP on {HOST}:{PORT}")

SessionLocal = sessionmaker(bind=engine)

def handle_request(client_connection):
    session = SessionLocal()
    try:
        request = client_connection.recv(1024).decode()
        print("Request received:\n", request)

        result = session.query(User).first()
        response_content = f"<html><body><h1>Data from DB: {result}</h1></body></html>"
        response = f"HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n{response_content}"
        
        client_connection.sendall(response.encode())
    except Exception as e:
        print("Error handling request:", e)
    finally:
        client_connection.close()
        session.close()
try:
    while True:
        client_connection, client_address = server_socket.accept()
        print(f"Connection from {client_address}")
        handle_request(client_connection)
except KeyboardInterrupt:
    print("\nServer shutting down.")
finally:
    cursor.close()
    database_connection.close()
    server_socket.close()