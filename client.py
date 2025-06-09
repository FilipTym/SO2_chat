import socket
import threading
import tkinter as tk
from tkinter import simpledialog, scrolledtext, messagebox

HOST = '127.0.0.1'
PORT = 8084

class ChatClient:
    def __init__(self, master):
        self.master = master
        self.master.title("Chat Client")
        self.master.geometry("500x400")

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        try:
            self.sock.connect((HOST, PORT))
        except Exception as e:
            messagebox.showerror("Connection Error", f"Could not connect: {e}")
            self.master.destroy()
            return

        self.nickname = self.ask_nickname()
        if not self.nickname:
            self.master.destroy()
            return

        try:
            self.sock.send(self.nickname.encode())
        except Exception as e:
            messagebox.showerror("Send Error", f"Failed to send nickname: {e}")
            self.master.destroy()
            return

        self.chat_area = scrolledtext.ScrolledText(master, state='disabled', bg="black", fg="lime", font=("Consolas", 11))
        self.chat_area.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        self.entry = tk.Entry(master)
        self.entry.pack(padx=10, pady=(0, 10), fill=tk.X)
        self.entry.bind("<Return>", self.send_message)

        threading.Thread(target=self.receive_messages, daemon=True).start()

    def ask_nickname(self):
        return simpledialog.askstring("Nickname", "Enter your nickname:", parent=self.master)

    def receive_messages(self):
        while True:
            try:
                data = self.sock.recv(1024).decode()
                if not data:
                    raise ConnectionError  # pusty string = zamknięcie socketu
                self.display_message(data)
            except:
                self.display_message("[Disconnected] Server closed the connection.\n")
                self.sock.close()
                self.master.quit()  # zamyka GUI
                break

    def send_message(self, event=None):
        message = self.entry.get().strip()
        if not message:
            return
        try:
            self.sock.send(message.encode())
            if message == "/quit":
                self.master.quit()
        except:
            self.display_message("[Error] Failed to send message.\n")
        self.entry.delete(0, tk.END)

    def display_message(self, message):
        self.chat_area.configure(state='normal')
        self.chat_area.insert(tk.END, message)
        self.chat_area.configure(state='disabled')
        self.chat_area.yview(tk.END)

if __name__ == "__main__":
    root = tk.Tk()
    client = ChatClient(root)
    root.mainloop()
