import socket
import threading

IP = socket.gethostbyname(socket.gethostname())
PORT = 5566
ADDR = (IP, PORT)
SIZE = 1024
FORMAT = "utf-8"
DISCONNECT_MESSAGE = "!DISCONNECT"

clients = []
def send_msg(conn, addr):
    print(f"[NEW CONNECTION] {addr} connected.")
    for client in clients:
        if client["addr"] != addr:
            conn.send(f"({client['addr'][0]} {client['addr'][1]}) connected to server".encode(FORMAT))
    for client in clients:
        if client["addr"] != addr:
            client["conn"].send(f"\n({addr[0]} {addr[1]}) connected to server".encode(FORMAT))

    connected = True
    while connected:
        msg = conn.recv(SIZE).decode(FORMAT)
        if msg == DISCONNECT_MESSAGE:
            connected = False
            for client in clients:
                if client["addr"] != addr:
                    client["conn"].send(f"\n({addr[0]} {addr[1]}) disconnected from server".encode(FORMAT))
            for client in clients:
                if client["addr"] == addr:
                    clients.remove(client)
                    break
            else:
                print(f"[ERROR] Cannot disconnect {addr}")
            print(f"\r[DISCONNECT CONNECTION] {addr} disconnected.")
        else:
            addrs =(msg.split(':')[0], int(msg.split(':')[1]))
            msg = msg.split(':')[2]
            msg = f"[{addr}] {msg}"
            for client in clients:
                if client["addr"] == addrs:
                    try:
                        client["conn"].send(msg.encode(FORMAT))
                        conn.send("Message sent".encode(FORMAT))
                    except BrokenPipeError:
                        print(f"[ERROR] Cannot send message to {addrs}")
                    break
    conn.close()

def main():
    print("[STARTING] Server is starting...")
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(ADDR)
    server.listen()
    print(f"[LISTENING] Server is listening on {IP}:{PORT}")

    while True:
        conn, addr = server.accept()
        clients.append({"addr":addr, "conn":conn})
        thread = threading.Thread(target=send_msg, args=(conn,addr))
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.active_count() - 1}")

if __name__=="__main__":
    main()