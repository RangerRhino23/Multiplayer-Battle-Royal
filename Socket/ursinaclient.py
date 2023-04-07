import socket
import threading
from ursina import *
import assets.APIs.player_moevement_api as pma

# Define host and port to connect to
HOST = 'localhost'
PORT = 25565

window.borderless = False
app = Ursina()

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
            global otherPlayer_position
            string_position = message.decode('utf-8')
            position = string_position.split(',')
            x = float(position[0].strip())
            y = float(position[1].strip())
            z = float(position[2].strip())
            otherPlayer_position = Vec3(x,y,z)

# Create a separate thread to receive messages from the server
receive_thread = threading.Thread(target=receive_messages)
receive_thread.start()

#################
###Ursina Code###
#################

class Player(Entity):
    def __init__(self,y=0,x=0, color=color.white, **kwargs):
        super().__init__(self, **kwargs)
        self.color = color
        self.y = y
        self.x = x
        self.model = 'circle'
        self.scale = 0.25

#Variables
positionCoodownSpeed = 0.01
positionCooldown = 0
sendPlayerPosition = True
otherPlayer_position = Vec3(0,0,0)

player = Player(y=0.5,x=0.5,color=color.red)

otherPlayer = Player(position=otherPlayer_position, color=color.green)

def input(key):
    if key == 'q':
        client_socket.close()
    if key == 'g':
        playerPosition = str(player.position)
        playerPosition = playerPosition.replace("Vec3(", "").replace(")", "")
        client_socket.send(playerPosition.encode('utf-8'))

def update():
    global positionCoodownSpeed,positionCooldown
    #Send Player Position to Server
    if sendPlayerPosition:
        positionCooldown += time.dt
        if positionCooldown >= positionCoodownSpeed:
            positionCooldown = 0
            playerPosition = str(player.position)
            playerPosition = playerPosition.replace("Vec3(", "").replace(")", "")
            client_socket.send(playerPosition.encode('utf-8'))
    
    #Moves otherPlayer to coords sent from Server
    otherPlayer.position = otherPlayer_position

    #Moves player around
    pma.player_movement(player, 2)

app.run()