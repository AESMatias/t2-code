import os
import sys
from PyQt6.QtCore import QObject, pyqtSignal, QThread
import socket
from threading import Thread

project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
carpeta_superior = os.path.join(project_root, "..")
sys.path.append(carpeta_superior)


class EstablecerSocket(QObject):
    message_received = pyqtSignal(str)

    def __init__(self, sender, host, port):
        super().__init__()
        self.sender= sender
        self.host = host
        self.port = port
        self.socket_cliente = socket.socket(
            socket.AF_INET, socket.SOCK_STREAM)
        self.enviar_mensaje_socket = socket.socket(
            socket.AF_INET, socket.SOCK_STREAM)

    def send_message(self, message: str) -> None:
        self.enviar_mensaje_socket.send(message.encode('utf-8'))

    def receive_messages(self,message) -> None:
        try:
            while True:
                data = self.socket_cliente.recv(4096)
                if not data:
                    self.socket_cliente.close()
                    self.enviar_mensaje_socket.close()
                    break
                elif data:
                    data = data.decode('utf-8', 'big')
                    print(f"Data recibida: {data}")
                    self.message_received.emit(data)
        except Exception as e:
            print("Error de tipo Exception:", e)
    def run_client(self) -> None:
        try:
            # un socket para enviar mensajes, y otro para recibir, asó
            #evitamos bloqueos en la transferencia de la informacion
            self.socket_cliente.connect((self.host, self.port))
            self.enviar_mensaje_socket.connect((self.host, self.port))
            receive_thread = Thread(target=self.receive_messages)
            receive_thread.start()

        except ConnectionError as e:
            print('Error de conexión', e)
            self.socket_cliente.close()
            self.enviar_mensaje_socket.close()


class ThreadCliente(QThread):
    def __init__(self, communicator):
        super().__init__()
        self.communicator = communicator

    def run(self):
        self.communicator.run_client()

def nivel_aumentado(sender):
    EstablecerSocket.send_message('level_up')
    
def connect_user(self,sender):
    pass

def send_message(self, message: str) -> None:
    pass
    # self.enviar_mensaje_socket.send(message.encode('utf-8'))
    
