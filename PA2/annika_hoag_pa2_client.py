import sys #use for reading information as command line arguments
from socket import *

import threading #to run processes concurrently


# Function to receive message from the server
def receive_message(client_socket):

    # At the same time, receive messages broadcast by server and display in terminal as they arrive
    new_message = client_socket.recv(1024)
    print(new_message.decode())



def main():
    # Accept hostname, port number, and username as command line arguments
    server_name = sys.argv[1]
    server_port = int(sys.argv[2])
    user_name = sys.argv[3]

    # Create client socket
    client_socket = socket(AF_INET, SOCK_STREAM)

    # Connect socket
    client_socket.connect((server_name, server_port))

    while True:
        # Create thread for connections
        t = threading.Thread(target=receive_message, args=(client_socket,), daemon=True)
        t.start()

        # Read lines of text from std input and send to server
        # message = input("Please enter your message: ")
        message = '[' + user_name + ']: '+ input()
        client_socket.send(message.encode())



if __name__ == "__main__":
    main()