import socket


def main():
    HOST = "localhost"
    PORT = 4221
    SERVER_ADDRESS = (HOST, PORT)
    CRLF = "\r\n"
    HTTP_STATUS_OK_RESPONSE = f"HTTP/1.1 200 OK"
    HTTP_STATUS_NOT_FOUND_RESPONSE = f"HTTP/1.1 404 Not Found"
    HTTP_CONTENT_TYPE_TEXT_PLAIN_RESPONSE = f"Content-Type: text/plain"
    BUFFER_SIZE = 1024

    server_socket = socket.create_server(SERVER_ADDRESS, reuse_port=True)
    conn, addr = server_socket.accept()

    with conn:
        print(f"Connected by {addr}")
        while True:
            data = conn.recv(BUFFER_SIZE).decode()
            if not data: break
            
            request = data.split(f"{CRLF}")
            start_line = request[0].split()
            path = start_line[1]

            if path == "/":
                conn.sendall(f"{HTTP_STATUS_OK_RESPONSE}{CRLF}{CRLF}".encode())
            elif path.startswith("/echo"):
                content_response = path.replace("/echo/", "")
                
                body = ""
                body += HTTP_STATUS_OK_RESPONSE + CRLF
                body += HTTP_CONTENT_TYPE_TEXT_PLAIN_RESPONSE + CRLF
                body += f"Content-Length: {len(content_response)}" + CRLF + CRLF
                body += content_response + CRLF

                conn.sendall(body.encode())
            else:
                conn.sendall(f"{HTTP_STATUS_NOT_FOUND_RESPONSE}{CRLF}{CRLF}".encode())


if __name__ == "__main__":
    main()
