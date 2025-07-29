import tkinter as tk
from server import start_server
import threading
import socket

def get_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(('10.255.255.255', 1))
        IP = s.getsockname()[0]
    except:
        IP = '127.0.0.1'
    finally:
        s.close()
    return IP

def run_server():
    ip = ip_entry.get()
    port = int(port_entry.get())
    info_label.config(text=f"Servidor rodando em {ip}:{port}")
    threading.Thread(target=start_server, args=(ip, port), daemon=True).start()

root = tk.Tk()
root.title("Servidor - Simulador de Chat")

tk.Label(root, text="IP para rodar o servidor:").pack()
ip_entry = tk.Entry(root)
ip_entry.insert(0, get_ip())
ip_entry.pack()

tk.Label(root, text="Porta:").pack()
port_entry = tk.Entry(root)
port_entry.insert(0, "5000")
port_entry.pack()

tk.Button(root, text="Iniciar Servidor", command=run_server).pack()
info_label = tk.Label(root, text="")
info_label.pack()

root.mainloop()
