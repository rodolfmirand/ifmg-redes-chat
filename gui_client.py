import tkinter as tk
from client import Client

# Global para guardar nome de usuário
username_global = ""

def connect():
    global username_global
    ip = ip_entry.get()
    port = int(port_entry.get())
    username = name_entry.get()
    if not username.strip():
        status_label.config(text="Informe um nome de usuário.")
        return

    username_global = username
    chat_frame.pack(fill=tk.BOTH, expand=True)
    connect_frame.pack_forget()

    username_label.config(text=username)

    global client
    client = Client(ip, port, username, gui)

def send_message():
    msg = message_entry.get()
    if msg:
        client.send(msg)
        message_entry.delete(0, tk.END)

def update_user_list(user_data):
    user_listbox.delete(0, tk.END)
    for user in user_data:
        name, status = user.split(':')
        user_listbox.insert(tk.END, f"{name} ({status})")

def display_message(msg):
    # Substituir nome do usuário pelo "Você" apenas se for mensagem pública
    if msg.startswith(f"{username_global}:"):
        msg = msg.replace(f"{username_global}:", "Você:", 1)
    elif msg.startswith(f"[PRIVADO] {username_global}:"):
        msg = msg.replace(f"[PRIVADO] {username_global}:", "[PRIVADO] Você:", 1)

    chat_text.config(state=tk.NORMAL)
    chat_text.insert(tk.END, msg + "\n")
    chat_text.config(state=tk.DISABLED)
    chat_text.see(tk.END)

class GuiStub:
    def update_user_list(self, data): update_user_list(data)
    def display_message(self, msg): display_message(msg)

gui = GuiStub()

root = tk.Tk()
root.title("Cliente - Simulador de Chat")

# Tela de conexão
connect_frame = tk.Frame(root)
connect_frame.pack(pady=10)

tk.Label(connect_frame, text="IP do servidor").pack()
ip_entry = tk.Entry(connect_frame)
ip_entry.insert(0, "127.0.0.1")
ip_entry.pack()

tk.Label(connect_frame, text="Porta do servidor").pack()
port_entry = tk.Entry(connect_frame)
port_entry.insert(0, "5000")
port_entry.pack()

tk.Label(connect_frame, text="Seu nome de usuário").pack()
name_entry = tk.Entry(connect_frame)
name_entry.pack()

tk.Button(connect_frame, text="Conectar", command=connect).pack(pady=5)
status_label = tk.Label(connect_frame, text="", fg="red")
status_label.pack()

# Tela de chat
chat_frame = tk.Frame(root)

# Label de identificação
username_label = tk.Label(chat_frame, text="", font=("Arial", 10, "bold"), fg="blue")
username_label.pack(pady=5)

chat_text = tk.Text(chat_frame, state=tk.DISABLED, width=50, height=20)
chat_text.pack(side=tk.LEFT, padx=5, pady=5)

right_frame = tk.Frame(chat_frame)
right_frame.pack(side=tk.LEFT, fill=tk.Y)

message_entry = tk.Entry(right_frame, width=40)
message_entry.pack(padx=5, pady=5)

send_button = tk.Button(right_frame, text="Enviar", command=send_message)
send_button.pack(padx=5)

tk.Label(right_frame, text="Usuários Online/Offline").pack(pady=5)
user_listbox = tk.Listbox(right_frame)
user_listbox.pack(padx=5, pady=5, fill=tk.BOTH, expand=True)

root.mainloop()
