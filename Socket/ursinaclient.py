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

otherPlayer = Player(color=color.blue,x=-0.5,y=-0.5)

#########################
###Socket Server Stuff###
#########################
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# Connect to the server
client_socket.connect((HOST, PORT))

# Receive client ID from the server
client_id = client_socket.recv(1024).decode('utf-8')
print(f'Client:{client_id}')

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

#Variables
positionCooldownSpeed = 2
positionCooldown = 0

def input(key):
    if key == 'g':
        print(f"OtherPlayer:{otherPlayer.position}")
    if key == 'f':
        print(f'Player:{player.position}')

def update():
    global positionCooldown,positionCooldownSpeed
    positionCooldown += time.dt
    if positionCooldown >= positionCooldownSpeed:
        positionCooldown = 0
        print(player.position)
        # Send message to the server
        position = str(player.position)
        client_socket.send(position.encode('utf-8'))
    pma.player_movement(player, 2)


app.run()