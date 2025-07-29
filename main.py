import subprocess
from server import start_server

def start():
    print("=== SIMULADOR DE WHATSAPP ===")
    print("1 - Iniciar como servidor (host)")
    print("2 - Iniciar como cliente")
    choice = input("Escolha (1 ou 2): ")

    if choice == '1':
        ip = input("Informe o IP para o servidor (ex: 127.0.0.1): ")
        port = int(input("Informe a porta (ex: 5000): "))
        print(f"[INFO] Servidor rodando em {ip}:{port}")
        start_server(ip, port)  # direto no terminal

    elif choice == '2':
        subprocess.call(['python', 'gui_client.py'])

    else:
        print("Escolha inválida.")

if __name__ == '__main__':
    start()
