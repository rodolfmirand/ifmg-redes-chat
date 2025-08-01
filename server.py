import socket
import threading

clients = {}  # {username: (conn, addr, online)}
message_history = []  # Lista de tuplas: (id, autor, texto)
message_id_counter = 1
lock = threading.Lock()

def broadcast(message, sender=None):
    for user, (conn, _, online) in clients.items():
        if online:
            try:
                conn.sendall(message.encode('utf-8'))
            except:
                pass

def private_message(target, message):
    if target in clients and clients[target][2]:
        conn = clients[target][0]
        try:
            conn.sendall(message.encode('utf-8'))
        except:
            pass

def handle_client(conn, addr):
    try:
        username = conn.recv(1024).decode('utf-8')
    except:
        conn.close()
        return

    clients[username] = (conn, addr, True)
    print(f"[+] {username} conectou de {addr[0]}:{addr[1]}")
    broadcast(f"{username} entrou no chat.")
    update_users()

    while True:
        try:
            msg = conn.recv(1024).decode('utf-8')
            if msg.startswith('/apagar '):
                try:
                    _, id_str = msg.split(' ', 1)
                    target_id = int(id_str.strip())
                    with lock:
                        for i, (mid, autor, texto) in enumerate(message_history):
                            if mid == target_id:
                                message_history[i] = (mid, autor, f"Mensagem de {autor} apagada por {username}")
                                broadcast(f"[{mid}] Mensagem de {autor} apagada por {username}")
                                break
                        else:
                            private_message(username, f"[Servidor]: Mensagem ID {target_id} não encontrada.")
                except:
                    private_message(username, "[Servidor]: Comando inválido. Use: /apagar [ID]")
                continue
            
            if msg.startswith('/editar '):
                try:
                    _, resto = msg.split(' ', 1)
                    id_str, novo_texto = resto.strip().split(' ', 1)
                    target_id = int(id_str.strip())

                    with lock:
                        for i, (mid, autor, texto) in enumerate(message_history):
                            if mid == target_id:
                                if autor != username:
                                    private_message(username, f"[Servidor]: Você só pode editar suas próprias mensagens.")
                                    break
                                message_history[i] = (mid, autor, novo_texto + " (editado)")
                                broadcast(f"[{mid}] {autor} (editado): {novo_texto}")
                                break
                        else:
                            private_message(username, f"[Servidor]: Mensagem ID {target_id} não encontrada.")
                except:
                    private_message(username, "[Servidor]: Comando inválido. Use: /editar [ID] nova mensagem")
                continue

            if not msg:
                break

            if msg.startswith('@'):
                target, _, content = msg.partition(' ')
                print(f"[PRIVADO] {username} -> {target[1:]}: {content}")
                private_message(target[1:], f"[PRIVADO] {username}: {content}")
            else:
                with lock:
                    global message_id_counter
                    message_id = message_id_counter
                    message_id_counter += 1
                    message_history.append((message_id, username, msg))
                    formatted = f"[{message_id}] {username}: {msg}"
                broadcast(formatted, sender=username)

        except:
            break

    clients[username] = (conn, addr, False)
    print(f"[-] {username} desconectou.")
    broadcast(f"{username} saiu do chat.")
    update_users()
    conn.close()

def update_users():
    user_list = ",".join([f"{u}:{'on' if online else 'off'}" for u, (_, _, online) in clients.items()])
    for conn, _, online in clients.values():
        if online:
            try:
                conn.sendall(f"@users {user_list}".encode('utf-8'))
            except:
                pass

def start_server(ip, port):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((ip, port))
    server.listen()
    print(f"[SERVIDOR] Rodando em {ip}:{port}")

    while True:
        conn, addr = server.accept()
        threading.Thread(target=handle_client, args=(conn, addr), daemon=True).start()
