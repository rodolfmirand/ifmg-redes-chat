import socket
import threading

clients = {}  # {username: (conn, addr, online)}

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
            if not msg:
                break

            if msg.startswith('@'):
                target, _, content = msg.partition(' ')
                print(f"[PRIVADO] {username} -> {target[1:]}: {content}")
                private_message(target[1:], f"[PRIVADO] {username}: {content}")
            else:
                print(f"[MENSAGEM] {username}: {msg}")
                broadcast(f"{username}: {msg}", sender=username)

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
