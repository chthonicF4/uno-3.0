
# modules , imports need to change based on the current working directory
import threading as thrd , pickle , queue as thrd_queue

if __name__ == "__main__" :
    import lib.networking as ntwk ,tkinter as tk ,CONFIG # networking functions and classes
    from lib.card import * # imports the classes used for cards and decks
    import card_gen # run card gen 

    
else :
    import main.lib.networking as ntwk , tkinter as tk , main.CONFIG as CONFIG # networking functions and classes
    from main.lib.card import * # imports the classes used for cards and decks
    import main.card_gen # run card gen 

# --------- WINDOW STUFF -------------

win_palete = CONFIG.win_palete

root = None

root = tk.Tk()
root.title(CONFIG.win_title)
root.geometry(f"{CONFIG.win_width}x{CONFIG.win_height}")
root.config(bg=win_palete[1])
root.columnconfigure(weight=1,index=0)
root.rowconfigure(weight=1,index=0)


class make_new_frame() :
    def __init__(self):
        self.frame = tk.Frame(
            master=root,
            width=CONFIG.win_width,
            height=CONFIG.win_height,
            bg=win_palete[1]
            )
        self.frame.columnconfigure(weight=1,index=0)
        self.frame.rowconfigure(weight=1,index=0)

    def pack(self):
        self.frame.grid(sticky=tk.NSEW)


CURRENT_FRAME = make_new_frame()
CURRENT_FRAME.pack()


# --------------------------THE CODE THAT ACTUALY DOES STUFF-----------------------------------


# ------- inital clients conecting ---------- (waiting for game to start)

entry_frame = tk.Frame(master=CURRENT_FRAME.frame,bg=CONFIG.win_palete[1])
CURRENT_FRAME.frame.columnconfigure(index=0,weight=1)
CURRENT_FRAME.frame.rowconfigure(index=0,weight=1)
entry_frame.grid(row=0,column=0)

class entry_box(): # class for info entry boxes
    def __init__(self,master,title:str,font,bg,fg,title_color,text_colour,box_width):
        self.frame = tk.Frame(master=master,width=1,height=1,bg=bg)
        self.box = tk.Entry(master=self.frame,fg=text_colour,font=font,bg=fg,width=box_width)
        self.title = tk.Label(master=self.frame,text=title,font=font,fg=title_color,bg=bg)
        self.frame.columnconfigure(index=1,weight=1)
        self.title.grid(column=0,row=0,padx=5,pady=2)
        self.box.grid(column=1,row=0,padx=5,pady=2)
    
    def get_box(self):
        return self.box.get()
    
    def dissable(self):
        self.box.config(state="disabled")

def on_info_submit(**k):
    global CURRENT_FRAME
    sock = ntwk.connection()
    # get sever addr 
    addr = server_address_box.get_box()
    #decode addr
    try:
        queue = thrd_queue.Queue()

        def recv_start_loop(sock,queue):
            while True:
                print("waiting for data")
                data = sock.recv()
                queue.put(data)

        seperator_index = addr.index(":")
        host , port = addr[:seperator_index] , int(addr[seperator_index+1:])
        sock.connect((host,port))
        sock.send(name_box.get_box())

        recv_start_loop_thread = thrd.Thread(target=recv_start_loop,daemon=True,name="Start recv thread",args=(sock,queue))
        recv_start_loop_thread.start()

    except :
        lable = "Server diddn't respond , make sure the address is correct"
        error_lable = tk.Label(master=entry_frame,text=lable,font=(CONFIG.win_font,10),fg="red",bg=CONFIG.win_palete[1])
        error_lable.grid(row=3,column=0)
    else:
        root.title(f"{CONFIG.win_title} {(host,port)} : {name_box.get_box()}")
        # make new frame saying connecting
        CURRENT_FRAME.frame.destroy()
        CURRENT_FRAME = make_new_frame()        
        lable = "Conected!"
        conecting_satus_msg = tk.Label(master=CURRENT_FRAME.frame,font=(CONFIG.win_font,20),text=lable,fg=CONFIG.win_palete[3],bg=CONFIG.win_palete[1])
        conecting_satus_msg.grid(row=0,column=0)
        CURRENT_FRAME.pack()
        #wait_till_start(sock,(host,port),queue)
        while True :
            try:
                print(queue.get_nowait())
            except:
                pass

# NAME INPUT 
lable = "Name :"
name_box = entry_box(
    entry_frame,
    f"{lable:>10}",
    (CONFIG.win_font,15),
    CONFIG.win_palete[1],
    CONFIG.win_palete[2],
    CONFIG.win_palete[0],
    CONFIG.win_palete[4],
    20
    )
name_box.box.config(insertbackground=CONFIG.win_palete[3])
name_box.frame.grid(row=0,column=0)

# server address
lable = "Address :"
server_address_box = entry_box(
    entry_frame,
    f"{lable:>10}",
    (CONFIG.win_font,15),
    CONFIG.win_palete[1],
    CONFIG.win_palete[2],
    CONFIG.win_palete[0],
    CONFIG.win_palete[4],
    20
    )
server_address_box.box.config(insertbackground=CONFIG.win_palete[3])
server_address_box.frame.grid(row=1,column=0)

# submit button 
lable = "submit"
submit_button = tk.Button(
    master=entry_frame,
    borderwidth=0,
    text=lable,
    bg=win_palete[2],
    font=(CONFIG.win_font,18),
    fg=win_palete[0],
    activebackground=win_palete[3],
    command=on_info_submit
    )
submit_button.grid(row=2,column=0,padx=20,pady=20)


def wait_till_start(sock,addr,queue):

    # wait unill recive "start" flag
    global CURRENT_FRAME

    CURRENT_FRAME.frame.destroy()
    CURRENT_FRAME = make_new_frame()
    lable = "Waiting for players to start" 

    waiting_room_frame = tk.Frame(master=CURRENT_FRAME.frame,width=1,height=1,bg=CONFIG.win_palete[1])

    waiting_lable = tk.Label(master=waiting_room_frame,font=(CONFIG.win_font,20),text=lable,fg=CONFIG.win_palete[3],bg=CONFIG.win_palete[1])
    lable = "PLAYERS"
    current_player_count = tk.Label(master=waiting_room_frame,font=(CONFIG.win_font,20),text=lable,fg=CONFIG.win_palete[3],bg=CONFIG.win_palete[1])
    CURRENT_FRAME.pack()
    waiting_room_frame.grid(row=0,column=0)

    
    waiting_lable.grid(row=0,column=0)
    current_player_count.grid(row=1,column=0)

    while True :
        try : 
            q_data , flag = queue.get_nowait()

            if flag == "disp":current_player_count.config(text=q_data)

            if flag == "start": 
                current_player_count.config(text=q_data)
                waiting_lable.config(text="Room Full")
                root.update()
                #break
        except:
            pass
        root.update()
    #main_loop(sock,addr,root,queue)

    

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

def main_loop(sock:ntwk.connection,server_addr,root:tk.Tk,recv_queue:thrd_queue.Queue) :
    global CURRENT_FRAME
    TEMP_PLAYER_HAND = []
    TEMP_DISCARD_PILE = []
    TEMP_PLAYERS_HAND_SIZES = []

    class card_img():
        def __init__(self,path,master):
            self.path = path
            self.canvas = tk.Canvas(master=master,width=166,height=265)
            self.img = tk.PhotoImage(file=path)
            self.canvas.create_image(83,135,image=self.img)

        def pack(self):
            self.canvas.pack()

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

        # disp cards on window

    print(sock)
    print(sock.adress,sock.sock,sock.server)

    while True : 
        # recive data 
        flag,msg = 3,2
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