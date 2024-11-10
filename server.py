import socket
from dotenv import load_dotenv
import urllib.parse

from sqlalchemy import text
from models.models import User, SessionLocal, Transaction
from response_content import response_content
from transfer_script import transfer_funds

load_dotenv()

HOST = '127.0.0.1'
PORT = 8080

# TCP socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind((HOST, PORT))
server_socket.listen(5)
print(f"Serving HTTP on {HOST}:{PORT}")

def handle_request(client_connection):
    session = SessionLocal()
    try:
        request = client_connection.recv(1024).decode()
        print("Request received:\n", request)
        error_message = None

        if request.startswith("POST"):
            headers, body = request.split("\r\n\r\n", 1)
            form_data = urllib.parse.parse_qs(body)

            source_account_id = int(form_data.get("source_account_id", [0])[0])
            target_account_id = int(form_data.get("target_account_id", [0])[0])
            amount = float(form_data.get("amount", [0])[0])

            try:
                transfer_funds(source_account_id, target_account_id, amount)
            except Exception as e:
                print("hey it is an error")
                error_message = str(e)

            transaction_data = session.query(Transaction).all()
            bank_user_data = session.execute(text("""
                SELECT a.id as account_id,b.name AS bank_name, u.first_name AS user_first_name, 
                       u.last_name AS user_last_name, a.account_type, a.balance
                FROM banks b
                JOIN accounts a ON b.id = a.bank_id
                JOIN users u ON a.user_id = u.id
            """)).fetchall()

            response = f"HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n{response_content(transaction_data, bank_user_data, error_message)}"

        else:
            transaction_data = session.query(Transaction).all()
            bank_user_data = session.execute(text("""
                SELECT a.id as account_id, b.name AS bank_name, u.first_name AS user_first_name, 
                       u.last_name AS user_last_name, a.account_type, a.balance
                FROM banks b
                JOIN accounts a ON b.id = a.bank_id
                JOIN users u ON a.user_id = u.id
            """)).fetchall()

            response = f"HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n{response_content(transaction_data, bank_user_data)}\r\n\r\n"

        client_connection.sendall(response.encode())
        client_connection.close()

    except Exception as e:
        print("Error:", e)
    finally:
        session.close()

try:
    while True:
        client_connection, client_address = server_socket.accept()
        print(f"Connection from {client_address}")
        handle_request(client_connection)
except KeyboardInterrupt:
    print("\nServer shutting down.")
finally:
    server_socket.close()