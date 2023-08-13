import socket
import threading
import sys
import os
from collections import namedtuple

IP_ADDRESS = ''
PORT_NUMBER = 53535
ADDRESS = (IP_ADDRESS, PORT_NUMBER)
MESSAGE_SIZE = 1024
MESSAGE_FORMAT = "utf-8"
DISCONNECT_SIGNAL = "QUIT!"

clients = []
ClientInfo = namedtuple("ClientInfo", ["connection", "address"])

current_input = None


def display_message(msg):
    if current_input is None:
        print(msg)
    else:
        print(f"\r{msg}\n{current_input}", end="")
        sys.stdout.flush()


def input_message(string):
    global current_input

    current_input = string
    result = input(string)
    current_input = None

    return result


def find_client_info(address):
    for client in clients:
        if client.address == address:
            return client
    return None


def send_to_clients():
    while True:
        addr_input = input_message("(ip:port)> ")
        if addr_input == DISCONNECT_SIGNAL:
            while clients:
                client = clients.pop()
                client.connection.send(DISCONNECT_SIGNAL.encode(MESSAGE_FORMAT))
            os._exit(0)

        try:
            addr_input = (addr_input.split(":")[0], int(addr_input.split(":")[1]))
        except (IndexError, ValueError):
            display_message(f"[ERROR] Invalid address {addr_input}")
            continue

        client = find_client_info(addr_input)
        if client is None:
            display_message(f"[ERROR] Client not found {addr_input}")
            continue

        msg_input = input_message("(msg)> ")

        try:
            client.connection.send(msg_input.encode(MESSAGE_FORMAT))
        except BrokenPipeError:
            display_message(f"[ERROR] Cannot send message to {addr_input}")


def handle_client(connection, address):
    display_message(f"[NEW CONNECTION] {address[0]}:{address[1]} connected.")

    connected = True
    while connected:
        msg = connection.recv(MESSAGE_SIZE).decode(MESSAGE_FORMAT)
        if msg == DISCONNECT_SIGNAL:
            connected = False

        display_message(f"[{address[0]}:{address[1]}] {msg}")
        try:
            connection.send("Message received".encode(MESSAGE_FORMAT))
        except BrokenPipeError:
            display_message(f"[ERROR] Cannot send message to {address}")
            connected = False

    display_message(f"[DISCONNECT CONNECTION] {address[0]}:{address[1]} disconnected.")
    display_message(f"[ACTIVE CONNECTIONS] {threading.active_count() - 3}")

    clients.remove(ClientInfo(connection, address))
    connection.close()


def main():
    display_message(f"[STARTING] Server is starting...")
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    server_socket.bind(ADDRESS)

    server_socket.listen()
    display_message(f"[LISTENING] Server is listening on {IP_ADDRESS}:{PORT_NUMBER}")

    display_message(f"[ACTIVE CONNECTIONS] {threading.active_count() - 1}")

    send_thread = threading.Thread(target=send_to_clients)
    send_thread.start()

    while True:
        connection, address = server_socket.accept()
        clients.append(ClientInfo(connection, address))

        client_thread = threading.Thread(target=handle_client, args=(connection, address))
        client_thread.start()

        display_message(f"[ACTIVE CONNECTIONS] {threading.active_count() - 2}")


if __name__ == "__main__":
    main()
