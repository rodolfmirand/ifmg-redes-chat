import subprocess

def start():
    print("=== SIMULADOR DE WHATSAPP ===")
    print("1 - Iniciar como servidor (host)")
    print("2 - Iniciar como cliente")
    choice = input("Escolha (1 ou 2): ")

    if choice == '1':
        subprocess.call(['python', 'gui_server.py'])
    elif choice == '2':
        subprocess.call(['python', 'gui_client.py'])
    else:
        print("Escolha inválida.")

if __name__ == '__main__':
    start()
