import tkinter as tk
from client import Client
import re

username_global = ""
message_line_positions = {}  # {ID: posição inicial no Text}

def connect():
    global username_global
    ip = ip_entry.get()
    port = int(port_entry.get())
    username = name_entry.get()
    if not username.strip():
        status_label.config(text="Informe um nome de usuário.")
        return

    username_global = username
    connect_frame.pack_forget()
    chat_frame.pack(fill=tk.BOTH, expand=True)
    username_label.config(text=f"Você: {username}")

    global client
    client = Client(ip, port, username, gui)

def send_message():
    msg = message_entry.get()
    if msg:
        client.send(msg)
        message_entry.delete(0, tk.END)

def update_user_list(user_data):
    user_text.config(state=tk.NORMAL)
    user_text.delete(1.0, tk.END)
    for user in user_data:
        name, status = user.split(':')
        color = 'green' if status == 'on' else 'red'
        user_text.insert(tk.END, f"{name} ({status})\n", color)
    user_text.config(state=tk.DISABLED)


def display_message(msg):
    global message_line_positions

    # Verifica se tem ID no formato [número]
    match = re.match(r'\[(\d+)\] (.+)', msg)
    if match:
        msg_id = int(match.group(1))
        content = match.group(2)

        # Substituições para mensagens públicas
        edit_suffix = " (editado)"
        if content.startswith(f"{username_global}{edit_suffix}:"):
            content = content.replace(f"{username_global}{edit_suffix}:", f"Você{edit_suffix}:", 1)
        elif content.startswith(f"{username_global}:"):
            content = content.replace(f"{username_global}:", "Você:", 1)

        # Substituições para mensagens privadas
        elif content.startswith(f"[PRIVADO] {username_global}{edit_suffix}:"):
            content = content.replace(f"[PRIVADO] {username_global}{edit_suffix}:", f"[PRIVADO] Você{edit_suffix}:", 1)
        elif content.startswith(f"[PRIVADO] {username_global}:"):
            content = content.replace(f"[PRIVADO] {username_global}:", "[PRIVADO] Você:", 1)

        formatted = f"[{msg_id}] {content}"

        chat_text.config(state=tk.NORMAL)

        if msg_id in message_line_positions:
            # Substituir linha existente
            line_index = message_line_positions[msg_id]
            chat_text.delete(f"{line_index}.0", f"{int(line_index)+1}.0")
            chat_text.insert(f"{line_index}.0", formatted + "\n")
        else:
            # Inserir nova linha e registrar posição
            line_index = int(chat_text.index("end-1c").split('.')[0])
            message_line_positions[msg_id] = line_index
            chat_text.insert(tk.END, formatted + "\n")

        chat_text.config(state=tk.DISABLED)
        chat_text.see(tk.END)
        return

    # Mensagens sem ID (como "João entrou no chat")
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
root.geometry("800x500")

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

top_frame = tk.Frame(chat_frame)
top_frame.pack(fill=tk.BOTH, expand=True)

# Área de mensagens (70% da largura)
messages_frame = tk.Frame(top_frame, width=550)
messages_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

username_label = tk.Label(messages_frame, text="", font=("Arial", 10, "bold"), fg="blue", anchor="w")
username_label.pack(fill=tk.X, padx=5, pady=5)

chat_text = tk.Text(messages_frame, state=tk.DISABLED, wrap=tk.WORD)
chat_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

# Lista de usuários (30% da largura)
users_frame = tk.Frame(top_frame, width=200)
users_frame.pack(side=tk.LEFT, fill=tk.Y)
users_frame.pack_propagate(False)  # Impede que o frame se ajuste ao conteúdo

tk.Label(users_frame, text="Usuários on/off", font=("Arial", 10, "bold")).pack(pady=5)
user_text = tk.Text(users_frame, height=10, state=tk.DISABLED)
user_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

user_text.tag_configure('green', foreground='green')
user_text.tag_configure('red', foreground='red')

# Campo de digitação e botão de envio
# Campo de digitação e botão de envio
bottom_frame = tk.Frame(chat_frame)
bottom_frame.pack(fill=tk.X, padx=5, pady=(0, 5))

# Instruções de edição/remoção
info_label = tk.Label(bottom_frame, text="Use /editar [ID] [nova mensagem] ou /apagar [ID]", font=("Arial", 8), fg="gray")
info_label.pack(anchor='w', padx=(0, 5))

entry_frame = tk.Frame(bottom_frame)
entry_frame.pack(fill=tk.X)

message_entry = tk.Entry(entry_frame)
message_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))

send_button = tk.Button(entry_frame, text="Enviar", command=send_message, width=10)
send_button.pack(side=tk.LEFT)


root.mainloop()
