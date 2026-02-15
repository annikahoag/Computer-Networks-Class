import sys #use for reading in command line arguments
from socket import * 
import threading 

client_list = []


# Function to send messages, we have this function so that we can do threading 
def send_message(connection_socket):
    try:
        message = b''
        while True:
            message = connection_socket.recv(1024)

            # Going through clients
            for client in client_list:
            
                # Send message to all connected clients (but not ourself)
                if client != connection_socket:
                    client.sendall(message)
    except:
        # If we hit an error, that means that we killed one of the connections, so remove the client  we're working with 
        client_list.remove(connection_socket)
        connection_socket.close()


def main():
    # Accept port number as a command line argument
    server_port = int(sys.argv[1])

    # Create TCP socket
    server_socket = socket(AF_INET, SOCK_STREAM)

    # Associate server port number with the socket, this is our welcoming socket
    server_socket.bind(('', server_port))

    # Bind listening socket to that port, wait and listen for client
    server_socket.listen(1)
    print("The server is ready to receive.")


    # Run until manual termination
    while True:
        # Accept incoming client connections
        connection_socket, addr = server_socket.accept()
        
        # Keep track of connections 
        client_list.append(connection_socket)

        # Create thread for connection 
        t = threading.Thread(target=send_message, args=(connection_socket,), daemon=True)
        t.start()



if __name__ == "__main__":
    main()