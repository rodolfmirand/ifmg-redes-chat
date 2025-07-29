import socket
import threading

class Client:
    def __init__(self, ip, port, username, gui):
        self.gui = gui
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((ip, port))
        self.sock.sendall(username.encode('utf-8'))
        threading.Thread(target=self.receive, daemon=True).start()

    def receive(self):
        while True:
            try:
                msg = self.sock.recv(1024).decode('utf-8')
                if not msg:
                    break
                if msg.startswith('@users '):
                    user_data = msg[7:].split(',')
                    self.gui.update_user_list(user_data)
                else:
                    self.gui.display_message(msg)
            except:
                break

    def send(self, message):
        try:
            self.sock.sendall(message.encode('utf-8'))
        except:
            pass
