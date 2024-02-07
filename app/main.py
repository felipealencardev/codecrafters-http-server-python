import socket
import threading


CRLF = "\r\n"
HTTP_STATUS_OK_RESPONSE = "HTTP/1.1 200 OK"
HTTP_STATUS_NOT_FOUND_RESPONSE = "HTTP/1.1 404 Not Found"
HTTP_CONTENT_TYPE_TEXT_PLAIN_RESPONSE = "Content-Type: text/plain"
HOST = "localhost"
PORT = 4221
SERVER_ADDRESS = (HOST, PORT)
BUFFER_SIZE = 1024

def main():
    while True:
        server_socket = socket.create_server(SERVER_ADDRESS, reuse_port=True)
        client_thread = threading.Thread(target=handle_client_connection, args=(server_socket,))
        client_thread.start()   

def handle_client_connection(server_socket):
    client_connection, address = server_socket.accept()
    with client_connection:
        print(f"Connected by {address}")
        data = client_connection.recv(BUFFER_SIZE).decode()
        request = data.split(CRLF)
        start_line = request[0].split()
        path = start_line[1]

        if path == "/":
            client_connection.sendall(f"{HTTP_STATUS_OK_RESPONSE}{CRLF}{CRLF}".encode())
        elif path.startswith("/echo"):
            content_response = path.replace("/echo/", "")
            send_response_body(client_connection, content_response)
        elif path.startswith("/user-agent"):
            user_agent = get_user_agent_from_request(request)
            send_response_body(client_connection, user_agent)
        else:
            client_connection.sendall(f"{HTTP_STATUS_NOT_FOUND_RESPONSE}{CRLF}{CRLF}".encode())

def get_user_agent_from_request(request):
    user_agent = ""
    for header in request:
        if "User-Agent" in header:
            user_agent = header.split(": ")
    return user_agent[1]

def build_response_body(content):
    body = ""
    body += HTTP_STATUS_OK_RESPONSE + CRLF
    body += HTTP_CONTENT_TYPE_TEXT_PLAIN_RESPONSE + CRLF
    body += f"Content-Length: {len(content)}" + CRLF + CRLF
    body += content + CRLF
    return body

def send_response_body(conn, content):
    body = build_response_body(content)
    conn.sendall(body.encode())

if __name__ == "__main__":
    main()
