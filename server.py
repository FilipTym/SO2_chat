import socket
import threading

# Adres IP i port, na którym serwer będzie nasłuchiwać
HOST = '127.0.0.1'
PORT = 8084

# Słownik przechowujący aktualnie połączonych klientów i ich nicki
clients = {}

# Lock (mutex) do bezpiecznego dostępu do słownika 'clients'
clients_lock = threading.Lock()

# Funkcja do rozsyłania wiadomości do wszystkich klientów (z opcją wykluczenia nadawcy)
def broadcast(message, exclude=None):
    with clients_lock:
        # Iterujemy po wszystkich klientach
        for client, nick in clients.items():
            # Pomijamy klienta, który wysłał wiadomość (jeśli podany)
            if client != exclude:
                try:
                    # Wysyłamy wiadomość (zakładamy kodowanie UTF-8)
                    client.send(message.encode())
                except:
                    # Jeśli nie uda się wysłać, to zamykamy i usuwamy klienta
                    client.close()
                    del clients[client]

# Funkcja uruchamiana w osobnym wątku obsługuje jednego klienta
def handle_client(conn, addr):
    try:
        # Odbieramy od klienta jego nick (pierwsza wiadomość po połączeniu)
        nickname = conn.recv(1024).decode().strip()
    except:
        # Jeśli nie uda się odebrać zamykamy połączenie
        conn.close()
        return

    # Dodajemy klienta do listy aktywnych użytkowników (zabezpieczone Lockiem)
    with clients_lock:
        clients[conn] = nickname

    # Informacja diagnostyczna na serwerze
    print(f"[Server] {nickname} connected from {addr}")

    # Wysyłamy wiadomość powitalną do innych klientów (ale nie do nowego)
    broadcast(f"[Server] {nickname} has joined the chat!\n", exclude=conn)

    # Wysyłamy informację tylko do nowego klienta
    conn.send("[Server] Connected! Type /quit to exit.\n".encode())

    # Główna pętla odbierająca wiadomości od klienta
    while True:
        try:
            msg = conn.recv(1024).decode()
            if msg.strip() == "/quit":
                # Jeśli klient wpisze /quit – rozłączamy go
                break
            # Rozsyłamy wiadomość do innych klientów
            broadcast(f"{nickname}: {msg}\n")
        except:
            # Jeśli nastąpi błąd odbioru (np. klient zamknął aplikację)
            break

    # Po opuszczeniu pętli klient się rozłącza
    with clients_lock:
        del clients[conn]  # Usuwamy go ze słownika

    conn.close()  # Zamykanie socketu

    # Informujemy pozostałych użytkowników o rozłączeniu klienta
    broadcast(f"[Server] {nickname} has left the chat.\n")

    # Logujemy rozłączenie na konsoli serwera
    print(f"[Server] {nickname} disconnected")

# Funkcja startująca główny serwer czatu
def start_server():
    # Tworzymy socket TCP (IPv4, strumieniowy)
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    # Przypisujemy IP i port do naszego socketu
    server.bind((HOST, PORT))

    # Zaczynamy nasłuchiwać połączeń
    server.listen()
    print(f"[Server] Listening on {HOST}:{PORT}...")

    # Nieskończona pętla serwer cały czas działa
    while True:
        # Czekamy na nowego klienta blokujące wywołanie
        conn, addr = server.accept()

        # Dla każdego nowego klienta uruchamiamy osobny wątek
        threading.Thread(target=handle_client, args=(conn, addr), daemon=True).start()

# Uruchamiamy serwer, jeśli plik został uruchomiony bezpośrednio
if __name__ == "__main__":
    start_server()
