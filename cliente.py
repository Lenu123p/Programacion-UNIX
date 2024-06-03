import socket
import os

def send_file(file_path):
    # Crear un socket TCP/IP
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Conectar el socket al servidor
    server_address = ('localhost', 65432)
    print("Intentando conectar al servidor...")
    client_socket.connect(server_address)
    print("Conectado al servidor.")

    try:
        # Información del archivo
        file_size = os.path.getsize(file_path)
        file_name = os.path.basename(file_path)
        file_info = f"{file_name},{file_size}"

        # Enviar información del archivo
        print(f"Enviando información del archivo: {file_info}")
        client_socket.sendall(file_info.encode())

        # Abrir el archivo en modo lectura binaria
        with open(file_path, 'rb') as file:
            # Leer el archivo en bloques y enviarlos
            while True:
                data = file.read(1024)
                if not data:
                    break
                client_socket.sendall(data)
            print("Archivo enviado correctamente.")

        # Enviar mensaje de finalización
        client_socket.sendall(b'DONE')
        print("Mensaje de finalización enviado.")
    finally:
        client_socket.close()
        print("Conexión cerrada.")

if __name__ == "__main__":
    file_path = r'C:\Users\vale ruiz\SOCKET\cliente.py'  # Reemplaza esto con la ruta de tu archivo
    send_file(file_path)