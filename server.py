import lib.networking as ntwk , random
import time

from lib.loading_bars import loadingbar as ldngbr

# classes

from lib.card import *
               
# ----------------------- CARD STUFF -----------------------

# card propertys
colours = ["red","blue","green","yellow"]
numbers = ["1","2","3","4","5","6","7","8","9","+2"]*2 + ["0","skip"]
special = ["+4","wild"]*4

# card functions 

def gen_deck():
    out = deck()
    ID_counter = 0
    for colour in colours :
        for numb in numbers :
            out.add(card(colour,numb,ID_counter))
            ID_counter += 1
    for type in special :
        out.add(card("black",type,ID_counter))
        ID_counter += 1
    return out

# ----------------------- NETWORKING -----------------------

# ---- network flags ----
#
# disp : message send from server to be displayed by client to user
# start : tells clients the game is  starting 
#
#


# networikng functions
def brodcast(msg,flag):
    for client_conn in clients:
        client_conn.send(msg,flag)
        time.sleep(0.05)

# setup
server_conn = ntwk.connection()
server_addr = server_conn.bind()
print(f"{server_addr[0]}:{server_addr[1]}")
clients = []
# await for all players to join
room_size = int(input("room size (2 minimum) : ")) # numb between 2

print("waiting for clients")

while len(clients) < room_size :
    # keep acepting connections till room is full , then start game

    client_conn , client_addr = server_conn.listen()
    print(client_addr)
    clients.append(client_conn)
    bar = ldngbr(len(clients)/room_size,room_size,"PLAYERS")
    brodcast(f"{bar}\r","disp")
print("starting")
brodcast("game starting","start")

# ------------------ GAME CODE 4REAL -----------------------

# ----- init ------

pickup_pile = gen_deck()
pickup_pile.shuffle()


class player() : 

    def __init__(self,conn,hand:deck,):
        self.conn = conn
        self.hand = hand
        pass

    def pick_up(self):
        self.hand.add(pickup_pile.take())

# create the player list and populate with the players

players = []
for client in clients : players.append(player(client,deck()))

# hand out cards to each 

number_of_cards = 7

for gamer in players :
    # give cards
    for handout in range(number_of_cards): 
        gamer.pick_up()


# ---- functions -----



