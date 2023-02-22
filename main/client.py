
# modules

if __name__ == "__main__" :
    import lib.networking as ntwk ,tkinter as tk ,CONFIG # networking functions and classes
    from lib.card import * # imports the classes used for cards and decks
    import card_gen

    
else :
    import main.lib.networking as ntwk , tkinter as tk , main.CONFIG as CONFIG # networking functions and classes
    from main.lib.card import * # imports the classes used for cards and decks
    import main.card_gen

# --------- WINDOW STUFF -------------

win_palete = CONFIG.win_palete

root = tk.Tk()
root.title(CONFIG.win_title)
root.geometry(f"{CONFIG.win_width}x{CONFIG.win_height}")
root.config(bg=win_palete[1])
root.columnconfigure(weight=1,index=0)
root.rowconfigure(weight=1,index=0)


class make_new_frame() :
    def __init__(self):
        self.frame = tk.Frame(master=root,width=CONFIG.win_width,height=CONFIG.win_height,bg=win_palete[1])

    def pack(self):
        self.frame.grid(sticky=tk.NSEW)



CURRENT_FRAME = make_new_frame()
CURRENT_FRAME.pack()



# -------- PRESET VARIABLES ----------




# Functions
def connect_to_a_server():
    sock = ntwk.connection()
    # get sever addr 
    addr = str(input(("Address : ")))
    #decode addr
    seperator_index = addr.index(":")
    host , port = addr[:seperator_index] , int(addr[seperator_index+1:])
    #try to connect to server
    try : 
        sock.connect((host,port))
    except :
        print(("Server diddn't respond , make sure the address is correct"))
        connect_to_a_server()
    return sock , (host,port)




# --------------------------THE CODE THAT ACTUALY DOES STUFF-----------------------------------


# ------- inital clients conecting ---------- (waiting for game to start)

# get a nickname then join server


# NAME INPUT 
name_box = 




sock , server_addr = connect_to_a_server()

sock.send(nickname,"nickname")

# wait unill recive "start" flag
print(f"\nWaiting for players to start :")
while True:
    data = sock.recv()
    if data[1] == "start" : break
    print(data[0],end="")
    
print(data[0])

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
    print("\n")
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
    print(TEMP_DISCARD_PILE.deck[0].disp_name)



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
    
    # CLOSE data = close reason 
    
    elif flag == "close" :
        sock.close()
        print(f"<server> : {msg}")
        break
        pass
    
    # DISPLAY
    
    elif flag == "disp" :
        print(f"\n{msg}")
    
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
                print("invalid choice please choose again <client>")
            else : 
                break


        sock.send(id_choice,"chooseCard")
    
    
    # CHOOSE A COLOUR 

    elif flag == "chooseColour" :
        colours = msg
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
        
        sock.send(chosen_colour_index,"chooseColour")

    else :
        pass