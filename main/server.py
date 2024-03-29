
if __name__ == "__main__" :
    import lib.networking as ntwk , random , time , threading , PIL , CONFIG
    from lib.loading_bars import loadingbar as ldngbr
    from lib.card import *
else:
    import main.lib.networking as ntwk , random , time , threading , PIL , main.CONFIG as CONFIG
    from main.lib.loading_bars import loadingbar as ldngbr
    from main.lib.card import *

# config 

SETTINGS = CONFIG.SETTINGS


# megga plus 4 , plus 4's everyone 

# ----------------------- CARD STUFF -----------------------

# card propertys
colours = ["red","blue","green","yellow"]
numbers = ["1","2","3","4","5","6","7","8","9","+2"]*2 + ["0","skip","reverse"]
special = ["+4","wild"]*4

if SETTINGS["+10"] == True :
    special.append("+10")

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
# gameUpdate : client should display the hand data
# chooseCard : tells client to choose a card and send back the card id
# nickname : client sending nickname to server
# chooseColour : client needs to pick a colour
# turnend : tells the client their turn is over
#
#


# networikng functions
def brodcast(msg,flag):
    print(f"brocasting : {(msg,flag)}")
    for client_conn in clients:
        client_conn[0].send(msg,flag)
        time.sleep(0.05)
        print(f"\---- {client_conn},{msg,flag}")

def client_handle(conn):
    global clients
    nickname = "Player"
    try:
        while True:
            data,flag = conn.recv()
            if flag == "close" :
                conn_close_reason = data
                break
            elif flag == "nickname" :
                for index , client in enumerate(clients) :
                    if client[0] == conn :
                        clients[index][1] = data
                        nickname = data
                        break
        return


    except:
        conn_close_reason = "due to connection error"
    
    # when connection closes print message and close connection
    print(f"{conn.adress} disscoected {conn_close_reason}")
    clients.pop(clients.index((conn,nickname)))
    pass

# setup
server_conn = ntwk.connection()
server_addr = server_conn.bind()
print(f"{server_addr[0]}:{server_addr[1]}")
clients = []
# await for all players to join
room_size = int(input("room size (2 minimum) : ")) # numb more than 2

print("waiting for clients")

while True :


    # keep acepting connections till room is full , then start game

    client_conn , client_addr = server_conn.listen() # wait for more people

    print(client_addr) # print conn


    nickname , flag = client_conn.recv() # recv nick


    clients.append([client_conn,nickname]) # add to list

    time.sleep(CONFIG.network_delay)

    # check all clients are still connected
    for index,client in enumerate(clients) :
        try:
            client[0].send("PING","ping")
        except:
            clients.pop(index)


    if len(clients) == room_size: break # if room is full

    brodcast(ldngbr(len(clients)/room_size,10,"PLAYERS"),"disp") # send loading bar to clients

    time.sleep(CONFIG.network_delay)

brodcast("Game is starting","start")
print(clients)
time.sleep(CONFIG.action_delay)
# ------------------ GAME CODE 4REAL -----------------------

# ----- init ------

pickup_pile = gen_deck()
pickup_pile.shuffle()
discard_pile = deck()
discard_pile.add(pickup_pile.take())

class player() : 

    def __init__(self,conn,hand:deck,nickname):
        self.conn = conn
        self.hand = hand
        self.nick = nickname
        pass

    def pick_up(self):
        self.hand.add(pickup_pile.take())

# create the player list and populate with the players

players = []
for client in clients : players.append(player(client[0],deck(),client[1]))

# hand out cards to each 

number_of_cards = 7


def game_Update_for_client(client:player):
    # returns a list consisting of a list of all players and therir hand counts (including their own) their hand and the discard pile
    # [
    # [(player1_nick , hand size),(player2_nick , hand size) ect],
    #  client's hand 
    #  discard_pile
    # ]
    out = []
    for player in players :
        out.append((player.nick,len(player.hand.deck)))
    out = [out,client.hand,discard_pile]
    return out

def game_update():
    for player in players :
        game_update_info = game_Update_for_client(player)
        player.conn.send(game_update_info,"gameUpdate")

# send each player their hand and the discard pile
game_update()
for handout in range(number_of_cards):
    for gamer in players :
        # give cards 
        gamer.pick_up()
        time.sleep(CONFIG.action_delay)
        game_update()

### #### ### ## ## ## # # # # # # # # # # # ## 

# ----------- GAME VARS ----------------
TURN_POINTER = 0
CURRENT_ADDITTON_COUNTER = 0
TURN_POINTER_STEP = 1


# --------- FUNCTIONS ------------
def can_place_card(card1:card,card2:card): #reurns bool , if 2 cards are compatible
    global TURN_POINTER, CURRENT_ADDITTON_COUNTER

    if card1.colour == card2.colour or card1.colour == "black" : # same colour
        return True
    
    elif card1.type == card2.type : # same number / type
        if card1.type[0] == "+": # if card is a plus 4 or 2 then add to the cumulitve count 
            CURRENT_ADDITTON_COUNTER += int(card1.type[-1])
        return True
    
def request_card_choice(conn:ntwk.connection):
    # send request to client
    print(f"requesting card from player {conn}")
    time.sleep(CONFIG.action_delay)
    while True :
        conn.send("","chooseCard")
        data = conn.recv()
        if data[1] == 'confirm' :
            break
        time.sleep(CONFIG.network_delay)
    data = conn.recv()
    print(data)
    return data[0]


def client_choose_colour(conn):
    print(f"requesting colour from {conn}")
    conn.send(colours,"chooseColour")
    data = conn.recv()
    print(data)
    return data


action_delay = CONFIG.action_delay

def client_turn() : # executed the stuff for a clients turn (which client is passed into the function as a player object)
    global CURRENT_ADDITTON_COUNTER, TURN_POINTER , TURN_POINTER_STEP , players , discard_pile

    client = players[TURN_POINTER]
    chosen_card = None


    if CURRENT_ADDITTON_COUNTER != 0 : # if there is a + card or stack of them , check if client can add to the stack
        # check what kind of stack it is by looking at top card in the discard pile
        stack_type = discard_pile.deck[0].type

        can_add_to_stack = False

        # check if can add to stack , if not then add the stack count to the clients hand and the continue
        for card in client.hand.deck :
            if card.type == stack_type :
                can_add_to_stack = True
                break
        
        if SETTINGS["+ stacking"] == False :
            can_add_to_stack = False

        if can_add_to_stack != True :

            # add the current addition count to clients hand
            for addition in range(CURRENT_ADDITTON_COUNTER) :
                players[TURN_POINTER].pick_up()
                game_update()
                time.sleep(action_delay)
            CURRENT_ADDITTON_COUNTER = 0
            return
        
        else: # if can add to the stack, request a card choice from the client
            
            while True :
                chosen_id = request_card_choice(client.conn)

                # if card id is -1 then make player add addtion counter to their hand
                if chosen_id == -1 :
                    for addition in range(CURRENT_ADDITTON_COUNTER) :
                        players[TURN_POINTER].pickup()
                        game_update()
                        time.sleep(action_delay)
                    break


                index_of_chosen_card = int(client.hand.find_by_id(chosen_id))
                chosen_card = client.hand.deck[index_of_chosen_card]

                if chosen_card.type == stack_type : # if card has the same type as the stack type
                    
                    #play the card and add to the stack count
                    discard_pile.add(client.hand.take(index_of_chosen_card))
                    CURRENT_ADDITTON_COUNTER += int(stack_type[-1])
                    break
                else:
                    client.conn.send("Cant play that card","disp")
        
                    
    else: # request a card choice from client

        while True :
        
            chosen_id = request_card_choice(client.conn)
            
            if type(chosen_id) != int : # if the id is not an iteger try again
                client.conn.send("server revied bad choice , please try again","disp")
                continue


            if chosen_id == -1 : # if id is -1 then draw from the pile 
                players[TURN_POINTER].pick_up()
                break

            else : # if choice is not to draw 

                # check if is a valid choice

                index_of_chosen_card = client.hand.find_by_id(chosen_id)

                if index_of_chosen_card == None : # bad recv of data so try again
                    client.conn.send("server did not revive the choice , please try again","disp")
                    continue
                
                chosen_card = client.hand.deck[index_of_chosen_card]
                
                if can_place_card(chosen_card,discard_pile.deck[0]) : # if move is valid
                    discard_pile.add(client.hand.take(index_of_chosen_card))
                    
                    # check if card has special propertys

                    if chosen_card.type[0] == "+" :
                        CURRENT_ADDITTON_COUNTER += int(chosen_card.type[-1])
                    elif chosen_card.type == "skip" :
                        TURN_POINTER += TURN_POINTER_STEP
                    elif chosen_card.type == "reverse" :
                        TURN_POINTER_STEP = 0-TURN_POINTER_STEP
                    elif SETTINGS["7-0"] == True :
                        if chosen_card.type == "0" :
                            pass
                        elif chosen_card.type == "7" :
                            pass


                    break
                else :
                    client.conn.send("cant play that card right now","disp")
                    continue

        client.conn.send(chosen_id,"turnend")
        time.sleep(CONFIG.network_delay)


    # once card has been placed check if the card is black , if it is then get the client to choose a colour
    if discard_pile.deck[0].colour == "black" :
        game_update()
        chosen_colour = client_choose_colour(client.conn)
        print(f"chosen colour : {colours[chosen_colour[0]]}")
        discard_pile.deck[0].update(colour = colours[chosen_colour[0]]) 

    game_update()
    time.sleep(CONFIG.network_delay)

# server turn loop

def player_has_won(): # checks to see if a player has 0 cards , if so then returns player name , otherwise returns false
    for player in players :
        if len(player.hand.deck) == 0 :
            return player.nick
    return False

def play_main_loop():
    global TURN_POINTER , CURRENT_ADDITTON_COUNTER

    if discard_pile.deck[0].colour == "black" : # if the first card in the discard pile is black then set it to a random colour
        discard_pile.deck[0].colour = colours[random.randint(0,len(colours)-1)]
    
    while player_has_won() == False :
        clients_turn = players[TURN_POINTER].nick
        brodcast(f"it is {clients_turn}'s turn","disp")
        client_turn()
        time.sleep(CONFIG.action_delay)
        TURN_POINTER += TURN_POINTER_STEP
        if abs(TURN_POINTER) >= len(players) :
            TURN_POINTER = (TURN_POINTER%len(players))*len(players)
        time.sleep(action_delay)
    
    brodcast(f" {player_has_won()} has won","disp")
    brodcast("server is closing","close")

play_main_loop()

