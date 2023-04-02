import socket
import threading
from ursina import *
import assets.APIs.player_moevement_api as pma

# Define host and port to connect to
HOST = 'localhost'
PORT = 25565

window.borderless = False
app = Ursina()
class Player(Entity):
    def __init__(self,y=0,x=0, color=color.white, **kwargs):
        super().__init__(self, **kwargs)
        self.color = color
        self.y = y
        self.x = x
        self.model = 'circle'
        self.scale = 0.25



#########################
###Socket Server Stuff###
#########################
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# Connect to the server
client_socket.connect((HOST, PORT))

# Receive client ID from the server
client_id = client_socket.recv(1024).decode('utf-8')
print(f'Client: {client_id}')
print("Raw Client: " + client_id)
def receive_messages():
    while True:
        # Receive incoming message from the server
        message = client_socket.recv(1024)
        if message:
            otherPosition = message.decode('utf-8')
            print('updating otherPlayers position')
            otherPlayer.position = otherPosition

# Create a separate thread to receive messages from the server
receive_thread = threading.Thread(target=receive_messages)
receive_thread.start()


#################
###Ursina Code###
#################

player = Player(color=color.red,x=0.5,y=0.5)
otherPlayer = Player(color=color.blue,x=-0.5,y=-0.5)

def update():
    if client_id == str(1):
        pma.player_movement(player, 2)
        playerOnePos = str(player.position)
        client_socket.send(playerOnePos.encode('utf-8'))
    elif client_id == str(2):
        pma.player_movement(otherPlayer, 2)
        playerTwoPos = str(otherPlayer.position)
        client_socket.send(playerTwoPos.encode('utf-8'))



app.run()