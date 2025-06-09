import socket
import threading

HOST = '127.0.0.1'
PORT = 8084

clients = {}
clients_lock = threading.Lock()

def broadcast(message, exclude=None):
    with clients_lock:
        for client, nick in clients.items():
            if client != exclude:
                try:
                    client.send(message.encode())
                except:
                    client.close()
                    del clients[client]

def handle_client(conn, addr):
    try:
        nickname = conn.recv(1024).decode().strip()
    except:
        conn.close()
        return

    with clients_lock:
        clients[conn] = nickname

    print(f"[Server] {nickname} connected from {addr}")
    broadcast(f"[Server] {nickname} has joined the chat!\n", exclude=conn)
    conn.send("[Server] Connected! Type /quit to exit.\n".encode())

    while True:
        try:
            msg = conn.recv(1024).decode()
            if msg.strip() == "/quit":
                break
            broadcast(f"{nickname}: {msg}\n")
        except:
            break

    with clients_lock:
        del clients[conn]
    conn.close()
    broadcast(f"[Server] {nickname} has left the chat.\n")
    print(f"[Server] {nickname} disconnected")

def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen()
    print(f"[Server] Listening on {HOST}:{PORT}...")

    while True:
        conn, addr = server.accept()
        threading.Thread(target=handle_client, args=(conn, addr), daemon=True).start()

if __name__ == "__main__":
    start_server()
