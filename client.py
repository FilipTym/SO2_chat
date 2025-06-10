import socket
import threading
import tkinter as tk
from tkinter import simpledialog, scrolledtext, messagebox

# Server connection settings
HOST = '127.0.0.1'
PORT = 8084

# Chat client class with GUI
class ChatClient:
    def __init__(self, master):
        # Initialize the main window
        self.master = master
        self.master.title("Chat Client")
        self.master.geometry("500x400")

        # Create TCP socket
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Attempt to connect to the server
        try:
            self.sock.connect((HOST, PORT))
        except Exception as e:
            messagebox.showerror("Connection Error", f"Could not connect: {e}")
            self.master.destroy()
            return

        # Prompt user for nickname
        self.nickname = self.ask_nickname()
        if not self.nickname:
            self.master.destroy()
            return

        # Send nickname to the server
        try:
            self.sock.send(self.nickname.encode())
        except Exception as e:
            messagebox.showerror("Send Error", f"Failed to send nickname: {e}")
            self.master.destroy()
            return

        # Create the chat display area (read-only)
        self.chat_area = scrolledtext.ScrolledText(
            master, state='disabled', bg="black", fg="lime", font=("Consolas", 11)
        )
        self.chat_area.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        # Create the message input field
        self.entry = tk.Entry(master)
        self.entry.pack(padx=10, pady=(0, 10), fill=tk.X)

        # Send message when pressing Enter
        self.entry.bind("<Return>", self.send_message)

        # Start background thread to receive messages from the server
        threading.Thread(target=self.receive_messages, daemon=True).start()

    # Prompt the user to enter a nickname
    def ask_nickname(self):
        return simpledialog.askstring("Nickname", "Enter your nickname:", parent=self.master)

    # Thread function to receive messages from the server
    def receive_messages(self):
        while True:
            try:
                data = self.sock.recv(1024).decode()
                if not data:
                    raise ConnectionError  # Empty message = closed socket
                self.display_message(data)
            except:
                self.display_message("[Disconnected] Server closed the connection.\n")
                self.sock.close()
                self.master.quit()
                break

    # Send message typed by the user
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

    # Display message in the chat window
    def display_message(self, message):
        self.chat_area.configure(state='normal')      # Unlock the field
        self.chat_area.insert(tk.END, message)        # Insert the message
        self.chat_area.configure(state='disabled')    # Lock it again
        self.chat_area.yview(tk.END)                  # Scroll to the bottom

# Start the GUI application
if __name__ == "__main__":
    root = tk.Tk()
    client = ChatClient(root)
    root.mainloop()
