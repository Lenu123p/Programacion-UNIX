import socket

def start_server():
    # Crear un socket TCP/IP
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Enlazar el socket a la dirección y puerto
    server_address = ('localhost', 65432)
    server_socket.bind(server_address)

    # Escuchar conexiones entrantes
    server_socket.listen(1)
    print("Esperando una conexión...")

    while True:
        # Esperar a que se conecte un cliente
        connection, client_address = server_socket.accept()
        try:
            print(f"Conexión desde: {client_address}")

            # Recibir información del archivo
            file_info = connection.recv(1024).decode()
            if not file_info:
                print("No se recibió información del archivo.")
                continue
            
            try:
                file_name, file_size = file_info.split(',')
                file_size = int(file_size)
            except ValueError:
                print(f"Información del archivo recibida en formato incorrecto: {file_info}")
                continue

            print(f"Recibiendo archivo: {file_name}, tamaño: {file_size} bytes")

            # Crear y abrir el archivo para escritura binaria
            with open(file_name, 'wb') as file:
                received_size = 0
                while received_size < file_size:
                    data = connection.recv(1024)
                    if not data:
                        break
                    file.write(data)
                    received_size += len(data)
            print(f"Archivo {file_name} recibido correctamente.")

            # Recibir mensaje de finalización
            final_message = connection.recv(1024)
            if final_message == b'DONE':
                print("Transferencia completada, cerrando conexión.")
                break
        finally:
            connection.close()
    server_socket.close()

if __name__ == "__main__":
    start_server()
