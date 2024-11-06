import socket
import psycopg2 # type: ignore
from dotenv import load_dotenv # type: ignore
import os

load_dotenv()

HOST = '127.0.0.1'
PORT = 8080

DB_HOST = os.getenv('DB_HOST')
DB_NAME = os.getenv('DB_NAME')
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')

# TCP socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))
server_socket.listen(5)
print(f"Serving HTTP on {HOST}:{PORT}")

try:
    database_connection = psycopg2.connect(
        host=DB_HOST,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD
    )
    cursor = database_connection.cursor()
    print("Connected to the database.")
except Exception as e:
    print("Error connecting to the database:", e)

def handle_request(client_connection):
    try:
        # Receive the request from the client
        request = client_connection.recv(1024).decode()
        print("Request received:\n", request)

        cursor.execute("SELECT * FROM company.department LIMIT 1;")
        result = cursor.fetchone() 
        response_content = f"<html><body><h1>Data from DB: {result}</h1></body></html>"
        response = f"HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n{response_content}"
        
        client_connection.sendall(response.encode())
    except Exception as e:
        print("Error handling request:", e)
    finally:
        client_connection.close()
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