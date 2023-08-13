import socket
import threading
import sys
import os

CLIENT_IP = socket.gethostbyname(socket.gethostname())
CLIENT_PORT = 53535
SERVER_ADDRESS = (CLIENT_IP, CLIENT_PORT)
MESSAGE_SIZE = 1024
MESSAGE_FORMAT = "utf-8"
DISCONNECT_SIGNAL = "QUIT!"


def handle_client_server(client_socket: socket.socket):
    connected = True
    while connected:
        try:
            received_msg = client_socket.recv(MESSAGE_SIZE).decode(MESSAGE_FORMAT)
        except OSError:
            return
        if received_msg == DISCONNECT_SIGNAL:
            connected = False

        if received_msg:
            print(f"\r[CLIENT] {received_msg}")
            print("> ", end="")
            sys.stdout.flush()
    print()

    print(f"[DISCONNECT CONNECTION] Client disconnected.")
    client_socket.close()
    os._exit(0)


def main():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(SERVER_ADDRESS)
    print(f"[CONNECTED] Client connected to {CLIENT_IP}:{CLIENT_PORT}")

    client_server_thread = threading.Thread(target=handle_client_server, args=(client_socket,))
    client_server_thread.start()

    connected = True
    while connected:
        msg = input("> ")
        client_socket.send(msg.encode(MESSAGE_FORMAT))
        if msg == DISCONNECT_SIGNAL:
            connected = False

    print(f"[DISCONNECTED] Client disconnected from {CLIENT_IP}:{CLIENT_PORT}")
    client_socket.close()


if __name__ == "__main__":
    main()
