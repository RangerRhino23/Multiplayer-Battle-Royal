from ursinanetworking import *

Server = UrsinaNetworkingServer('Localhost', 25565)
Easy = EasyUrsinaNetworkingServer(Server)

@Server.event
def onClientConnected(Client):
    Easy.create_replicated_variable(f"player_{Client.id}",{ "type" : "player", "id" : Client.id, "position" : (0, 0, 0), "rotation" : {0,0,0} })
    print(f"{Client} connected !")
    Client.send_message("GetId", Client.id)

@Server.event
def onClientDisconnected(Client):
    Easy.remove_replicated_variable_by_name(f"player_{Client.id}")