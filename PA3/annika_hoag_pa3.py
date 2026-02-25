import sys
from socket import *
import threading


# Function for receiving HTTP request message (reading and parsing) 
def receive_request(connection_socket):
    request = b''
    
    while True:
        # Make sure we read the entire request 
        request = connection_socket.recv(1024)
        while b'\r\n\r\n' not in request:
            request = request + connection_socket.recv(1024)

        # Call function to figure out which get request we need to make
        get_manager(request.decode(), connection_socket)



# Decipher what GET is in our request (identify requested path)
def get_manager(request, connection_socket):

    if 'GET / ' in request:
        get_page(connection_socket)
    
    elif 'GET /index.html' in request:
        get_page(connection_socket)

    elif 'GET /internet.jpg' in request:
        get_image(connection_socket)
    
    else:
        get_error(connection_socket)



# HTTP response for getting index.html
def get_page(connection_socket):
    # Read information from index.html
    with open('index.html', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Send properly formatted response
    response = f'HTTP/1.1 200 OK\r\nConnection: close\r\nContent-Length: {len(content)}\r\nConnection-Type: text/html\r\n\r\n{content}'
    connection_socket.sendall(response.encode())



# HTTP response for getting internet.jpg
def get_image(connection_socket):
     # Read information from index.html
    with open('internet.jpg', 'rb') as f:
        content = f.read()
    
    # Send properly formatted response, encode the string first since image is already being encoded we don't want to encode everything like in get_page()
    response = (f'HTTP/1.1 200 OK\r\nConnection: close\r\nContent-Length: {len(content)}\r\nConnection-Type: image/jpeg\r\n\r\n').encode() + content
    connection_socket.sendall(response)



# HTTP response for getting error 
def get_error(connection_socket):
    # Create string with HTML code in it in place of reading an HTML file
    content = """
        <!doctype html><html>
        <head>
        <meta charset="utf-8">
        <title>Error</title>
        </head>
        <body>
        <h1>400 Bad Request</h1>
        </body>
        </html>
    """

    # Send properly formatted response
    response = f'HTTP/1.1 404 Not Found\r\nConnection: close\r\nContent-Length: {len(content)}\r\nConnection-Type: text/html\r\n\r\n{content}'
    connection_socket.sendall(response.encode())

    

def main():
    # Bind server to local host on specified port, start listening for TCP connections
    server_port = int(sys.argv[1])
    server_socket = socket(AF_INET, SOCK_STREAM)
    server_socket.bind(('', server_port))
    server_socket.listen(1)
    print("The server is ready to receive.")


    while True:
        # Accept TCP connection from browser
        connection_socket, addr = server_socket.accept()
        # print("connected to ", addr)

        # Create new thread when connecting to new browser
        browser_t = threading.Thread(target=receive_request, args=(connection_socket,), daemon=True)
        browser_t.start()




if __name__ == "__main__":
    main()