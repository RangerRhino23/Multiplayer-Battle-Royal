from ursina import *
from random import *
from ursinanetworking import *
import assets.APIs.player_moevement_api as pma



App = Ursina()
Client = UrsinaNetworkingClient('localhost',25565)
Easy = EasyUrsinaNetworkingClient(Client)
window.borderless = False

sky = Sky()

Players = {}
PlayersTargetPos={}

SelfId = -1

@Client.event
def GetId(Id):
    global SelfId
    SelfId = Id
    print(f"My ID is : {SelfId}") #sets and prints the current player id

@Easy.event
def onReplicatedVariableCreated(variable):
    global Client
    variable_name = variable.name
    variable_type = variable.content["type"]

    if variable_type == "player": #If its a player set all this up
        PlayersTargetPos[variable_name] = Vec2(0,0)
        if SelfId == int(variable.content["id"]):
            Players[variable_name].color = color.red
            Players[variable_name].visible = False

@Easy.event
def onReplicatedVariableUpdated(variable):
    PlayersTargetPos[variable.name] = variable.content["position"]

@Easy.event
def onReplicatedVariableRemoved(variable): #Doesn't really work atm but removes the player when disconneted 
    variable_name = variable.name
    variable_type = variable.content["type"]
    if variable_type == "player":
        destroy(Players[variable_name])
        del Players[variable_name]

Ply = Entity(model='circle', scale=0.25)

def Messages(key):
    Client.send_message("MyPosition", tuple(Ply.position))

Entity(input=Messages)
def update():
    pma.player_movement(Ply, 2)
    if Ply.position[1] < -5:
        Ply.position = (randrange(0, 15), 10, randrange(0, 15))
    for p in Players:
        try:
            Players[p].position += (Vec2(PlayersTargetPos[p]) - Players[p].position) / 25
        except Exception as e: print(e)
    
    Easy.process_net_events()

App.run()