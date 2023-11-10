import sys
import os
import socket
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_root)
from servidor.black_list import users_not_allowed
from servidor.funciones_servidor import usuario_permitido

print("aaaaaaaaaaaaaaaaaaa",project_root)
def main(host:int,port:int):
    # host y puerto obtenidos del archivo JSON

    # Crea un socket del servidor
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Vincula el socket a la dirección indiacada y el puerto
    server_socket.bind((host, port))

    # Comienza a escuchar conexiones entrantes
    server_socket.listen()

    print(f"Server listening on {host}:{port}")

    # Bucle While para mantener en continua escucha de conexiones entrantes
    while True:
        client_socket, client_address = server_socket.accept()
        print(f"Conexión entrante de {client_address}")
        # Maneja la conexión con el cliente
        client_data = client_socket.recv(1024)
        # decoded_data = pickle.loads(client_data)
        # message_serialized = serializar_mensaje(decoded_data)

        if not client_data:
            print(f'No data provided by the client: {client_address}')
            break
        client_data = client_data.decode('utf-8')
        if usuario_permitido(client_data, users_not_allowed) == False:
            print(f'Usuario no permitido: {client_address}')
            client_socket.send('False'.encode('utf-8'))
        print(' permitido pork ', usuario_permitido(client_data, users_not_allowed))
        # Procesa los datos del cliente (aquí puedes agregar tu lógica personalizada)
        # En este ejemplo, simplemente se envía una respuesta al cliente
        client_data = client_data.encode('utf-8')
        client_socket.send(client_data)
        client_socket.close()

    # Cierra el socket del servidor
    server_socket.close()
    
if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Debes usar: python main.py PORT, siendo PORT un entero.")
        sys.exit(1)

    port = int(sys.argv[1])
    host = 'localhost'  # Escucha en todas las interfaces de red

    main(host, port)