import socket


def main():
    HOST = "localhost"
    PORT = 4221
    SERVER_ADDRESS = (HOST, PORT)
    HTTP_STATUS_OK_RESPONSE = b"HTTP/1.1 200 OK\r\n\r\n"
    BUFFER_SIZE = 1024

    server_socket = socket.create_server(SERVER_ADDRESS, reuse_port=True)
    conn, addr = server_socket.accept()

    with conn:
        print(f"Connected by {addr}")
        while True:
            data = conn.recv(BUFFER_SIZE)
            if not data: break
            conn.sendall(HTTP_STATUS_OK_RESPONSE)


if __name__ == "__main__":
    main()
