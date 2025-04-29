import socket
import sqlite3
import datetime

# Se inicializa la base de datos
def setup_database():
    try:
        conn = sqlite3.connect("chat.db")
        cursor = conn.cursor()
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            contenido TEXT NOT NULL,
            fecha_envio TEXT NOT NULL,
            ip_cliente TEXT NOT NULL
        )""")
        conn.commit()
        return conn
    except sqlite3.Error as e:
        print(f"Error al configurar la base de datos: {e}")
        exit(1)

# Se configura el socket TCP/IP para escuchar conexiones
def initialize_server():
    try:
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind(("localhost", 5000))
        server_socket.listen(5)
        print("Servidor escuchando en localhost:5000")
        return server_socket
    except socket.error as e:
        print(f"Error al iniciar el servidor: {e}")
        exit(1)

# Manejo de la conexión de cada cliente
def handle_client(client_socket, db_conn, client_address):
    try:
        message = client_socket.recv(1024).decode("utf-8")
        if not message:
            return

        print(f"Mensaje recibido de {client_address}: {message}")
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Guardado del mensaje en la base de datos
        cursor = db_conn.cursor()
        cursor.execute("INSERT INTO messages (contenido, fecha_envio, ip_cliente) VALUES (?, ?, ?)",
                       (message, timestamp, client_address[0]))
        db_conn.commit()

        # Respuesta al cliente con un timestamp
        client_socket.send(f"Mensaje recibido: {timestamp}".encode("utf-8"))
    except Exception as e:
        print(f"Error manejando cliente {client_address}: {e}")
    finally:
        client_socket.close()

# Ciclo principal del servidor
def main():
    db_conn = setup_database()
    server_socket = initialize_server()

    while True:
        try:
            client_socket, client_address = server_socket.accept()
            print(f"Conexión aceptada de {client_address}")
            handle_client(client_socket, db_conn, client_address)
        except Exception as e:
            print(f"Error al aceptar conexiones: {e}")

if __name__ == "__main__":
    main()
