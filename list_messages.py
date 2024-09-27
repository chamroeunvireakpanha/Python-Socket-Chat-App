#list_messages.py
import socket

PORT = 5050
SERVER = "localhost"
ADDR = (SERVER, PORT)
FORMAT = "utf-8"
DISCONNECT_MESSAGE = "!DISCONNECT"


def connect():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(ADDR)
    return client


def start():
    connection = connect()
    print("Connected to the server. Listening for messages...")
    try:
        while True:
            msg = connection.recv(1024).decode(FORMAT)
            if msg == DISCONNECT_MESSAGE:
                print("Server has disconnected.")
                break
            print(msg)
    except:
        print("Connection closed or interrupted.")
    finally:
        connection.close()


start()
