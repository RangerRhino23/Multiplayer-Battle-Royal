from ursina import *
from network import Network
import assets.APIs.player_moevement_api as pma


app=Ursina()

clientNumber = 0


class Player(Entity):
    def __init__(self, x, y, width, height, **kwargs):
        super().__init__(self, **kwargs)
        self.x = x
        self.y = y
        self.scale_x = width
        self.scale_y = height

    def update(self):
        pma.player_movement(self, 2)

def read_pos(pos_str):
    if not pos_str:
        return 0, 0
    pos_list = pos_str.split(",")
    if len(pos_list) != 2:
        print("Invalid position string:", pos_str)
        return 0, 0
    try:
        x = int(pos_list[0])
        y = int(pos_list[1])
        return x, y
    except ValueError:
        print("Invalid position string:", pos_str)
        return 0, 0


def make_pos(tup):
    return str(tup[0]) + "," + str(tup[1])


n = Network()
startPos = read_pos(n.getPos())
p = Player(startPos[0],startPos[1],100,100)
p2 = Player(0,0,100,100)

def update():
    p2Pos = read_pos(n.send(make_pos((p.x, p.y))))
    p2.x = p2Pos[0]
    p2.y = p2Pos[1]
app.run()
