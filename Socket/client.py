import socket
import threading

# Define host and port to connect to
HOST = 'localhost'
PORT = 12343

# Create a socket object
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect to the server
client_socket.connect((HOST, PORT))

# Receive client ID from the server
client_id = client_socket.recv(1024).decode('utf-8')
print(client_id)

def receive_messages():
    while True:
        # Receive incoming message from the server
        message = client_socket.recv(1024)
        if message:
            print(message.decode('utf-8'))

# Create a separate thread to receive messages from the server
receive_thread = threading.Thread(target=receive_messages)
receive_thread.start()

while True:
    # Get input from the user
    message = input("")

    # Send message to the server
    client_socket.send(message.encode('utf-8'))
