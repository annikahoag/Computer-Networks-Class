import sys #use for reading information as command line arguments
from socket import *
import threading #to run processes concurrently


peer_list = [] #Keep track of all new connections 


# Function to physically send the message
def broadcast(message, connection_socket):
    # Send message to all connected peers except ourself
    for peer in peer_list:
        if peer != connection_socket:
            try:
                peer.sendall(message)
            except:
                peer_list.remove(peer)
                # peer.close()



# Function receive message 
def receive_message(connection_socket):

    message = b''
    while True:
        try:
            message = connection_socket.recv(1024)
            if message==b'':
                break

            # Display message when received
            print(message.decode())
        except:
            break
    # If we hit an error, that means that we killed one of the connections, so remove the peer we're working with 
    peer_list.remove(connection_socket)
    connection_socket.close()
        
    

# Function to connect seeding so that others can leech from us
def conn(seed_socket):
    while True:
        connection_socket, addr = seed_socket.accept()
        peer_list.append(connection_socket) #add new connection to list of peers 

        # Create thread so that multiple hosts can leech
        connect_t = threading.Thread(target=receive_message, args=(connection_socket,), daemon=True)
        connect_t.start()



def main():

    # Start peer program with a username, local listening port, and optional list of peer addressses
    user_name = sys.argv[1]
    listening_port = int(sys.argv[2])


    # Begin listening on port, seed_socket is on the end that takes connections 
    seed_socket = socket(AF_INET, SOCK_STREAM)
    seed_socket.bind(('', listening_port))
    seed_socket.listen()
    print("Ready to receive.")


    # for peer_address in peer_addresses:
    for i in range(3, len(sys.argv)):

        # Attempt to connect to each peer listed on command line (leeching)
        peer_address = sys.argv[i]
        splitted = peer_address.split(':')
        host_name = splitted[0]
        port_number = int(splitted[1])
        peer_socket = socket(AF_INET, SOCK_STREAM)
        peer_socket.connect((host_name, port_number))
        peer_list.append(peer_socket)

        # Send/receive messages over new and existing connections
        leeching_t = threading.Thread(target=receive_message, args=(peer_socket,), daemon=True)
        leeching_t.start()

    # Create thread so that we can open multiple seed sockets
    seeding_t = threading.Thread(target=conn, args=(seed_socket,), daemon=True)
    seeding_t.start()


    # User types message --> broadcast to all currently connected peers
    while True:
        # Read lines of text from std input and send to server
        message = '[' + user_name + ']: ' + input()
        
        # Send message to all connected peers except ourself
        broadcast(message.encode(), listening_port)
 



if __name__ == "__main__":
    main()