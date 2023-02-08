
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

sock , server_addr = connect_to_a_server()

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
#
#

TEMP_PLAYER_HAND = []

while True : 
    # recive data 
    msg,flag = sock.recv()

    if flag == "dispHand" :
        title = "YOUR HAND"
        print(f"{title:^18}")
        msg.display()
        TEMP_PLAYER_HAND = msg
        pass
    elif flag == "close" :
        sock.close()
        pass
    elif flag == "disp" :
        if data != ('game starting', 'start'):
            print(data)
    elif flag == "choseCard":
        # print hand and ask for card choice by id (also check if id is in hand)
        title = "YOUR HAND"
        print(f"{title:^18}")
        TEMP_PLAYER_HAND.display()
        
        ID_CHOICE = input(f"\nChoose a card to play")



    


    else :
        pass