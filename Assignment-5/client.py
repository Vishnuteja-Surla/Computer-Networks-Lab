import socket
import threading
import sys
import os

IP = socket.gethostbyname(socket.gethostname())
PORT = 5566
ADDR = (IP, PORT)
SIZE = 1024
FORMAT = "utf-8"
DISCONNECT_MESSAGE = "!DISCONNECT"


def handle_server(client):
    connected = True
    while connected:
        try:
            msg = client.recv(SIZE).decode(FORMAT)
        except OSError:
            return
        if msg == DISCONNECT_MESSAGE:
            connected = False

        else:
            file_name = "sample.txt"
            print(msg)
            file = open(file_name, "w")
            file.write(msg)
            file.close()
            print(f"\rFile received.")
            print("> ", end="")
            sys.stdout.flush()

    print(f"[DISCONNECTED] Client disconnected from {IP}:{PORT}]")
    client.close()
    os._exit(0)


def main():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(ADDR)
    print(f"[CONNECTED] Client connected to {IP}:{PORT}")

    server_thread = threading.Thread(target=handle_server, args=(client,))
    server_thread.start()

    connected = True
    while connected:
        file_name = input("> ")
        file = open(file_name, "r")
        msg = file.read()
        file.close()
        client.send(msg.encode(FORMAT))
        if msg == DISCONNECT_MESSAGE:
            connected = False

        msg = client.recv(SIZE).decode(FORMAT)
        if msg:
            print(f"[SERVER] {msg}")

    print(f"[DISCONNECTED] Client disconnected from {IP}:{PORT}")
    client.close()


if __name__ == "__main__":
    main()