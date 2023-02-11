
# modules

import lib.networking as ntwk # networking functions and classes

from lib.card import * # imports the classes used for cards and decks

import lib.colours as colrs

# -------- PRESET VARIABLES ----------

C_input = colrs.colrP(fg="lightcyan",ut="bold")
C_Warning = colrs.colrP(fg="lightred",ut="underline")
C_info = colrs.colrP(fg="yellow",ut="bold")

# Functions
def connect_to_a_server():
    sock = ntwk.connection()
    # get sever addr 
    addr = str(input(colrs.c("Address : ",cps=C_input)))
    #decode addr
    seperator_index = addr.index(":")
    host , port = addr[:seperator_index] , int(addr[seperator_index+1:])
    #try to connect to server
    try : 
        sock.connect((host,port))
    except :
        print(colrs.c("Server diddn't respond , make sure the address is correct",cps=C_info))
        connect_to_a_server()
    return sock , (host,port)




# --------------------------THE CODE THAT ACTUALY DOES STUFF-----------------------------------


# ------- inital clients conecting ---------- (waiting for game to start)

# get a nickname then join server
print(colrs.c("Name>> ",cps=C_input))
nickname = str(input())

sock , server_addr = connect_to_a_server()

sock.send(nickname,"nickname")

# wait unill recive "start" flag
print(f"\nWaiting for players to start :")
while True:
    data = sock.recv()
    if data[1] == "start" : break
    print(data[0],end="")
    
print(colrs.c(data[0],cps=C_info))

# ------- start game ---------------(when receve message that game is starting)

# start main listen loop from sever 

# ---- network flags ----
#
# disp : message send from server to be displayed by client to user
# start : tells clients the game is  starting 
# close : tells client to close connection / this connection is closing (msg half is to be displayed as reason) 
# dispHand : client should display the hand data
# choseCard : tells client to choose a card and send back the card id
# nickname : client sending nickname to server
#


TEMP_PLAYER_HAND = []
TEMP_DISCARD_PILE = []
TEMP_PLAYERS_HAND_SIZES = []

def display_game():
    # player hand sizes
    title = "CARD COUNT"
    print(f"{title:^18}")
    for player in TEMP_PLAYERS_HAND_SIZES :
        print(f"{player[1]:^3} : {player[0]}")
    title = "YOUR HAND"
    print(f"{title:^18}")
    TEMP_PLAYER_HAND.display()
    title = "DISCARD PILE"
    print(f"{title:^18}")
    TEMP_DISCARD_PILE.display()



while True : 
    # recive data 
    msg,flag = sock.recv()

    # GAME UPDATE

    if flag == "gameUpdate" :
        TEMP_PLAYERS_HAND_SIZES = msg[0]
        TEMP_PLAYER_HAND = msg[1]
        TEMP_DISCARD_PILE = msg[2]
        display_game()

        
        pass
    
    # CLOSE
    
    elif flag == "close" :
        sock.close()
        pass
    
    # DISPLAY
    
    elif flag == "disp" :
        if data != ('game starting', 'start'):
            print(data)
    
    # CHOOSE CARD
            
    elif flag == "chooseCard":
        # print hand and ask for card choice by id (also check if id is in hand)

        display_game()

        valid_choice = False
        while valid_choice != True :
            try :
                id_choice = int(input(f"\nChoose a card to play: "))
            except:
                print("that is not a number , please choose an id from above")
                continue
            for cards in TEMP_PLAYER_HAND.deck:
                if cards.ID == id_choice or id_choice == -1:
                    valid_choice = True
                    break
            if valid_choice == False :
                print("invalid choice please choose again")
            else : 
                break


        sock.send(id_choice,"chooseCard")
    
    
    # CHOOSE A COLOUR 

    elif flag == "chooseColour" :
        colours = data
        # print out options and take in choice as an index
        print(f"Choose a colour for card :\n")
        for index , colour in enumerate(colours) :
            print(f"[{index:<2}: {colour:<7}]")
        
        while True :
            try:
                chosen_colour_index = int(input("number >> "))
                chosen_colour = colour[chosen_colour_index]
            except:
                print("Invalid input, please choose a number from above.")
                continue
            break
        
        sock.send(chosen_colour,"chooseColour")

    else :
        pass