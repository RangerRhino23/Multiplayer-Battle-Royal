import socket
import threading

# Define host and port to listen on
HOST = '192.168.2.151'
PORT = 25565

# Create a socket object
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to a specific address and port
server_socket.bind((HOST, PORT))
print(f'Started Server on {HOST}:{PORT}')

# Listen for incoming connections
server_socket.listen()

# List to keep track of connected clients
clients = []

# Function to handle incoming client connections
def handle_client(sock, addr):
    # Send client ID to the client
    client_id = "Client ID: " + str(len(clients) + 1)
    sock.send(client_id.encode('utf-8'))

    # Add the client socket to the list of connected clients
    clients.append(sock)

    while True:
        try:
            # Receive incoming message from the client
            message = sock.recv(1024)
            
            if message:
                for client in clients:
                    if client != sock:
                        client.send(message)
                        
        except ConnectionResetError:
            # Handle case when client disconnects
            clients.remove(sock)
            print(f'Client {addr} disconnected')
            break

# Function to continuously listen for incoming connections
def listen_for_clients():
    while True:
        # Wait for incoming client connections
        sock, addr = server_socket.accept()
        print(f'Client {addr} connected')
        

        # Create a new thread to handle the incoming client connection
        client_thread = threading.Thread(target=handle_client, args=(sock, addr))
        client_thread.start()

# Start listening for incoming connections
listen_for_clients()
