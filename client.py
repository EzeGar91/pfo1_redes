import socket

# Conectar al servidor
def connect_to_server():
    try:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect(("localhost", 5000))
        print("Conexión exitosa al servidor.")
        return client_socket
    except socket.error as e:
        print(f"Error al conectar al servidor: {e}")
        exit(1)

# Enviar mensaje al servidor
def send_messages(client_socket):
    while True:
        message = input("Escribe tu mensaje (o 'éxito' para salir): ")
        if message.lower() == "éxito":
            print("Cerrando conexión...")
            break
        try:
            client_socket.send(message.encode("utf-8"))
            response = client_socket.recv(1024).decode("utf-8")
            print(f"Respuesta del servidor: {response}")
        except Exception as e:
            print(f"Error al enviar/recibir datos: {e}")
            break
    client_socket.close()

def main():
    client_socket = connect_to_server()
    send_messages(client_socket)

if __name__ == "__main__":
    main()
