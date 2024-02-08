import socket
import threading
import sys
import os


CRLF = "\r\n"
HTTP_STATUS_OK_RESPONSE = "HTTP/1.1 200 OK"
HTTP_STATUS_NOT_FOUND_RESPONSE = "HTTP/1.1 404 Not Found"
HTTP_CONTENT_TYPE_TEXT_PLAIN = "text/plain"
HTTP_CONTENT_TYPE_OCTET_STREAM = "application/octet-stream"
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
        directory_path = get_directory_path()

        if path == "/":
            client_connection.sendall(f"{HTTP_STATUS_OK_RESPONSE}{CRLF}{CRLF}".encode())
        elif path.startswith("/echo"):
            content_response = path.replace("/echo/", "")
            send_response_body(client_connection, 
                               content_response, 
                               HTTP_CONTENT_TYPE_TEXT_PLAIN)
        elif path.startswith("/user-agent"):
            user_agent = get_user_agent_from_request(request)
            send_response_body(client_connection, 
                               user_agent, 
                               HTTP_CONTENT_TYPE_TEXT_PLAIN)
        elif directory_path != "" and path.startswith("/files"):
            filename = path.replace("/files/", "")
            file_path = os.path.join(directory_path, filename)
            if os.path.isfile(file_path):
                try:
                    with open(file_path, "rb") as file:
                        file_contents = file.read()
                        send_response_body(client_connection, 
                                           file_contents.decode(), 
                                           HTTP_CONTENT_TYPE_OCTET_STREAM)
                except IOError as error:
                    raise Exception(f"Could not open the file. Error: {error}")
            else:
                send_not_found_response(client_connection)
        else:
            send_not_found_response(client_connection)

def send_not_found_response(client_connection):
    client_connection.sendall(f"{HTTP_STATUS_NOT_FOUND_RESPONSE}{CRLF}{CRLF}".encode())

def get_user_agent_from_request(request):
    user_agent = ""
    for header in request:
        if "User-Agent" in header:
            user_agent = header.split(": ")
    return user_agent[1]

def build_response_body(content, content_type):
    body = ""
    body += HTTP_STATUS_OK_RESPONSE + CRLF
    body += "Content-Type: " + content_type + CRLF
    body += f"Content-Length: {len(content)}" + CRLF + CRLF
    body += content + CRLF
    return body

def send_response_body(conn, content, content_type):
    body = build_response_body(content, content_type)
    print("body")
    print(body)
    conn.sendall(body.encode())

def get_directory_path():
    directory_path = ""
    if "--directory" in sys.argv:
        directory_index = sys.argv.index("--directory") + 1
        if directory_index < len(sys.argv):
            directory_path = sys.argv[directory_index]
            
    return directory_path

if __name__ == "__main__":
    main()
