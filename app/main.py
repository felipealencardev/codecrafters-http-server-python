import socket


def main():
    HOST = "localhost"
    PORT = 4221
    SERVER_ADDRESS = (HOST, PORT)
    HTTP_STATUS_OK_RESPONSE = b"HTTP/1.1 200 OK\r\n\r\n"
    HTTP_STATUS_NOT_FOUND_RESPONSE = b"HTTP/1.1 404 Not Found\r\n\r\n"
    BUFFER_SIZE = 1024

    server_socket = socket.create_server(SERVER_ADDRESS, reuse_port=True)
    conn, addr = server_socket.accept()

    with conn:
        print(f"Connected by {addr}")
        while True:
            data = conn.recv(BUFFER_SIZE)
            if not data: break
            
            request_list = data.split(b"\r\n")
            start_line = request_list[0].split()
            path = start_line[1]
            
            if path == b"/":
                conn.sendall(HTTP_STATUS_OK_RESPONSE)
            else:
                conn.sendall(HTTP_STATUS_NOT_FOUND_RESPONSE)


if __name__ == "__main__":
    main()
