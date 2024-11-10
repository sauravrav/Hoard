import socket
from dotenv import load_dotenv
import urllib.parse
from models.models import User, SessionLocal
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

        if request.startswith("POST"):
            headers, body = request.split("\r\n\r\n", 1)
            form_data = urllib.parse.parse_qs(body)

            source_account_id = int(form_data.get("source_account_id", [0])[0])
            target_account_id = int(form_data.get("target_account_id", [0])[0])
            amount = float(form_data.get("amount", [0])[0])

            transfer_funds(source_account_id, target_account_id, amount)

            response = "HTTP/1.1 303 See Other\r\nLocation: /\r\n\r\n"

        else:
            response = f"HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n{response_content()}"
        
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
    server_socket.close()