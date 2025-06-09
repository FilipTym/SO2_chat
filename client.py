import socket
import threading
import tkinter as tk
from tkinter import simpledialog, scrolledtext, messagebox

# Ustawienia połączenia – ten sam adres i port co na serwerze
HOST = '127.0.0.1'
PORT = 8084

# Klasa reprezentująca klienta czatu z interfejsem graficznym
class ChatClient:
    def __init__(self, master):
        # Inicjalizacja głównego okna aplikacji
        self.master = master
        self.master.title("Chat Client")
        self.master.geometry("500x400")

        # Tworzymy socket klienta – TCP/IP
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Próba połączenia z serwerem
        try:
            self.sock.connect((HOST, PORT))
        except Exception as e:
            messagebox.showerror("Connection Error", f"Could not connect: {e}")
            self.master.destroy()
            return  # Kończymy, jeśli nie uda się połączyć

        # Pytanie użytkownika o nickname
        self.nickname = self.ask_nickname()
        if not self.nickname:
            self.master.destroy()
            return  # Jeśli użytkownik anuluje – zamykamy

        # Wysyłamy nickname do serwera
        try:
            self.sock.send(self.nickname.encode())
        except Exception as e:
            messagebox.showerror("Send Error", f"Failed to send nickname: {e}")
            self.master.destroy()
            return

        # Tworzymy pole do wyświetlania wiadomości (tylko do odczytu)
        self.chat_area = scrolledtext.ScrolledText(
            master, state='disabled', bg="black", fg="lime", font=("Consolas", 11)
        )
        self.chat_area.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        # Tworzymy pole do wpisywania wiadomości
        self.entry = tk.Entry(master)
        self.entry.pack(padx=10, pady=(0, 10), fill=tk.X)

        # Po naciśnięciu Enter wysyłamy wiadomość
        self.entry.bind("<Return>", self.send_message)

        # Uruchamiamy wątek odbierający wiadomości z serwera
        threading.Thread(target=self.receive_messages, daemon=True).start()

    # Funkcja pytająca użytkownika o nick (okno dialogowe)
    def ask_nickname(self):
        return simpledialog.askstring("Nickname", "Enter your nickname:", parent=self.master)

    # Wątek nasłuchujący wiadomości z serwera
    def receive_messages(self):
        while True:
            try:
                # Odbieramy dane z serwera
                data = self.sock.recv(1024).decode()
                if not data:
                    raise ConnectionError  # Brak danych = rozłączenie
                self.display_message(data)  # Wyświetlamy wiadomość
            except:
                # Obsługa błędu połączenia
                self.display_message("[Disconnected] Server closed the connection.\n")
                self.sock.close()
                self.master.quit()  # Zamykamy GUI
                break

    # Wysyłanie wiadomości wpisanej przez użytkownika
    def send_message(self, event=None):
        message = self.entry.get().strip()  # Pobieramy tekst z pola
        if not message:
            return  # Ignorujemy puste wiadomości
        try:
            self.sock.send(message.encode())  # Wysyłamy do serwera
            if message == "/quit":
                self.master.quit()  # Jeśli /quit – zamykamy aplikację
        except:
            self.display_message("[Error] Failed to send message.\n")
        self.entry.delete(0, tk.END)  # Czyścimy pole tekstowe

    # Wyświetlanie wiadomości w polu czatu
    def display_message(self, message):
        self.chat_area.configure(state='normal')     # Odblokowujemy pole
        self.chat_area.insert(tk.END, message)       # Dodajemy nową wiadomość
        self.chat_area.configure(state='disabled')   # Znowu blokujemy edycję
        self.chat_area.yview(tk.END)                 # Przewijamy do dołu

# Uruchomienie aplikacji tworzenie GUI
if __name__ == "__main__":
    root = tk.Tk()                 # Tworzymy główne okno aplikacji
    client = ChatClient(root)     # Inicjalizujemy klienta
    root.mainloop()               # Uruchamiamy główną pętlę zdarzeń (GUI)
