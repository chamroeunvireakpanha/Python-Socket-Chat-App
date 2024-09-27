#server.py
import threading
import socket
from datetime import datetime 

PORT = 5050
SERVER = "172.16.0.123"
ADDR = (SERVER, PORT)
FORMAT = "utf-8"
DISCONNECT_MESSAGE = "!DISCONNECT"

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

clients = set()
clients_lock = threading.Lock()


def handle_client(conn, addr):
    print(f"[NEW CONNECTION] {addr} Connected")

    try:
        connected = True
        while connected:
            try:
                msg = conn.recv(1024).decode(FORMAT)
                if not msg:
                    break

                if msg == DISCONNECT_MESSAGE:
                    connected = False
                
                # Add timestamp
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                broadcast_msg = f"[{addr} at {timestamp}] {msg}"
                print(broadcast_msg)
                broadcast(broadcast_msg, conn)
                ack_msg = f"[SERVER at {timestamp}] Message received"
                conn.sendall(ack_msg.encode(FORMAT))

            except socket.error as e:
                print(f"[CONNECTION ERROR] {addr} {e}")
                break


    finally:
        with clients_lock:
            clients.remove(conn)

        conn.close()
        print(f"[CONNECTION CLOSED] {addr}")

def broadcast(message, sender_conn=None):
    with clients_lock:
        for c in clients:
            if c != sender_conn:
                c.sendall(message.encode(FORMAT))
def start():
    print('[SERVER STARTED]!')
    server.listen()
    while True:
        conn, addr = server.accept()
        with clients_lock:
            clients.add(conn)
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()

def start_server_msg():
    while True:
        server_msg = input("Message from the server: ")
        if server_msg.lower() == 'q':
            break

        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        broadcast_msg = f"[SERVER at {timestamp}] {server_msg}"
        print(broadcast_msg)
        broadcast(broadcast_msg)

start()
