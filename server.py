import lib.networking as ntwk , random , time , threading

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
# close : tells client to close connection / this connection is closing (msg half is to be displayed as reason) 
# dispHand : client should display the hand data
# choseCard : tells client to choose a card and send back the card id
#
#


# networikng functions
def brodcast(msg,flag):
    print(f"brocasting : {(msg,flag)}")
    for client_conn in clients:
        client_conn.send(msg,flag)
        time.sleep(0.05)

def client_handle(conn):
    try:
        while True:
            data,flag = conn.recv()
            if flag == "close" :
                conn_close_reason = data
                break
    except:
        conn_close_reason = "due to connection error"
    
    # when connection closes print message and close connection
    print(f"{conn.adress} disscoected {conn_close_reason}")
    clients.pop(clients.index(conn))
    pass

# setup
server_conn = ntwk.connection()
server_addr = server_conn.bind()
print(f"{server_addr[0]}:{server_addr[1]}")
clients = []
# await for all players to join
room_size = int(input("room size (2 minimum) : ")) # numb more than 2

print("waiting for clients")

def player_bar_start(room_size): 
    temp_len = len(clients) 
    while True:

        if temp_len != len(clients):
            bar = ldngbr(len(clients)/room_size,room_size,"PLAYERS")
            brodcast(f"{bar}\r","disp")
            temp_len = len(clients)
        temp_len = len(clients)
        if temp_len == room_size :
            return
        time.sleep(0.02)

# start loading bar thread that will relay the ammount of players in queue
loading_bar_thread = threading.Thread(target=player_bar_start,args=(room_size,))
loading_bar_thread.start()


while len(clients) < room_size :
    # keep acepting connections till room is full , then start game
    client_conn , client_addr = server_conn.listen()
    print(client_addr)
    clients.append(client_conn)
    client_thread = threading.Thread(target=client_handle,args=(client_conn,))
    client_thread.name = client_addr
    client_thread.start()
print("starting")
brodcast("game starting","start")

# ------------------ GAME CODE 4REAL -----------------------

# ----- init ------

pickup_pile = gen_deck()
pickup_pile.shuffle()
discard_pile = deck()
discard_pile.add(pickup_pile.take())

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



# send each player their hand 
for gamer in players :
    gamer.conn.send(gamer.hand,"dispHand")


### #### ### ## ## ## # # # # # # # # # # # ## 

# ----------- GAME VARS ----------------
TURN_POINTER = 0
CURRENT_ADDITTON_COUNTER = 0


# --------- FUNCTIONS ------------
def can_place_card(card1:card,card2:card): #reurns bool , if 2 cards are compatible
    global TURN_POINTER, CURRENT_ADDITTON_COUNTER

    if card1.colour == card2.colour : # same colour
        return True
    
    elif card1.type == card2.type : # same number / type
        if card1.type == "+4" or card1.type == "+2" : # if card is a plus 4 or 2 then add to the cumulitve count 
            CURRENT_ADDITTON_COUNTER += int(card1.type[-1])
        return True
    
def request_card_choice(conn):

    pass


def client_turn() : # executed the stuff for a clients turn (which client is passed into the function as a player object)
    global CURRENT_ADDITTON_COUNTER, TURN_POINTER , players

    client = players[TURN_POINTER]
    
    if CURRENT_ADDITTON_COUNTER != 0 : # if there is a + card or stack of them , check if client can add to the stack
        # check what kind of stack it is by looking at top card in the discard pile
        stack_type = discard_pile[0].type

        can_add_to_stack = False

        # check if can add to stack , if not then add the stack count to the clients hand and the continue
        for card in client.hand :
            if card.type == stack_type :
                can_add_to_stack = True
                break
        
        if can_add_to_stack != True :
            for addition in range(CURRENT_ADDITTON_COUNTER) :
                players[TURN_POINTER].pickup()
            return
        else: # if can add to the stack request a card choice from the client
            pass







