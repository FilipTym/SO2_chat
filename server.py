import socket
import threading

# Server IP and port
HOST = '127.0.0.1'
PORT = 8084

# Dictionary to store connected clients and their nicknames
clients = {}

# Lock (mutex) to ensure thread-safe access to the 'clients' dictionary
clients_lock = threading.Lock()

# Function to broadcast messages to all connected clients (excluding the sender if specified)
def broadcast(message, exclude=None):
    with clients_lock:
        for client, nick in list(clients.items()):
            if client != exclude:
                try:
                    client.send(message.encode())
                except:
                    client.close()
                    del clients[client]

# Function that runs in a separate thread to handle a single client
def handle_client(conn, addr):
    try:
        # Receive client's nickname (first message after connecting)
        nickname = conn.recv(1024).decode().strip()
    except:
        conn.close()
        return

    # Add the client to the active users dictionary (with thread-safe lock)
    with clients_lock:
        clients[conn] = nickname

    # Log connection and inform other users
    print(f"[Server] {nickname} connected from {addr}")
    broadcast(f"[Server] {nickname} has joined the chat!\n", exclude=conn)

    # Send welcome message to the connected client
    conn.send("[Server] Connected! Type /quit to exit.\n".encode())

    # Main loop to receive and broadcast client messages
    while True:
        try:
            msg = conn.recv(1024).decode()
            if msg.strip() == "/quit":
                break
            broadcast(f"{nickname}: {msg}\n")
        except:
            break

    # Cleanup after client disconnects
    with clients_lock:
        del clients[conn]
    conn.close()
    broadcast(f"[Server] {nickname} has left the chat.\n")
    print(f"[Server] {nickname} disconnected")

# Starts the chat server
def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # TCP socket
    server.bind((HOST, PORT))  # Bind IP and port
    server.listen()  # Start listening for incoming connections
    print(f"[Server] Listening on {HOST}:{PORT}...")

    while True:
        conn, addr = server.accept()  # Wait for a new client
        threading.Thread(target=handle_client, args=(conn, addr), daemon=True).start()  # Handle client in a new thread

# Run the server when this file is executed directly
if __name__ == "__main__":
    start_server()
