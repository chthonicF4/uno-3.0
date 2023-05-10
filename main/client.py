
# modules , imports need to change based on the current working directory
import threading as thrd, queue as thrd_queue ,time ,os

if __name__ == "__main__" :
    import lib.networking as ntwk ,tkinter as tk ,CONFIG  ,lib.game_widgets as g_widgets# networking functions and classes
    from lib.card import * # imports the classes used for cards and decks 

    
else :
    import main.lib.networking as ntwk , tkinter as tk , main.CONFIG as CONFIG , main.lib.game_widgets as g_widgets # networking functions and classes
    from main.lib.card import * # imports the classes used for cards and decks

# --------- WINDOW STUFF -------------

# make the root var the window , add title from config , set base geometry and configs
root = tk.Tk()
root.title(CONFIG.win_title)
root.geometry(f"{CONFIG.win_width}x{CONFIG.win_height}")
root.config(bg=CONFIG.win_palete[1])
root.columnconfigure(weight=1,index=0)
root.rowconfigure(weight=1,index=0)
root_dir = os.path.dirname(os.path.realpath(__file__))
# define class that basicaly clears the winow in one go so i have a blank slate to work with.

class make_new_frame() :
    def __init__(self):
        self.frame = tk.Frame(
            master=root,
            width=CONFIG.win_width,
            height=CONFIG.win_height,
            bg=CONFIG.win_palete[1]
            )
        self.frame.columnconfigure(weight=1,index=0)
        self.frame.rowconfigure(weight=1,index=0)

    def pack(self):
        self.frame.grid(sticky=tk.NSEW)

# make a frame and pack it

CURRENT_FRAME = make_new_frame()
CURRENT_FRAME.pack()


# ---------------------------------------------------------------------------------------
##################### START OF ACCTUAL CODE (NOT JUST WINDOW SETUP) #####################
# ---------------------------------------------------------------------------------------


# ------- inital clients conecting ---------- (waiting for game to start)


# make frame for all of the wigites to be organised into and set its config.
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

# -------------------------- TO BE CALLED WHEN INFO IS SUBBMITED (name and server addr) -------------------------------------------------------------
def on_info_submit(**k):
    global CURRENT_FRAME
    sock = ntwk.connection()
    # get sever addr 
    addr = server_address_box.get_box()

    #decode addr 
    seperator_index = addr.index(":")
    host , port = addr[:seperator_index] , int(addr[seperator_index+1:])

    # try to connect to server 
    try :
        sock.connect((host,port))

    except :

        # show an error message and try again
        lable = "Server diddn't respond , make sure the address is correct"
        error_lable = tk.Label(master=entry_frame,text=lable,font=(CONFIG.win_font,10),fg="red",bg=CONFIG.win_palete[1])
        error_lable.grid(row=3,column=0)
        return
    
    # start listen thread
    queue = thrd_queue.Queue()
    def recv_thread_func(sock,queue:thrd_queue.Queue):
        while True :
            data  = sock.recv()
            queue.put_nowait(data)
    
    recv_thread = thrd.Thread(target=recv_thread_func,daemon=True,name="recv thread",args=(sock,queue))
    recv_thread.start()

    # send sever nickname
    sock.send(name_box.get_box())

    # ----- update window -----

    # update widnow name to include server addr and nickname of client
    root.title(f"{CONFIG.win_title} {(host,port)} : {name_box.get_box()}")

    # make new frame with connection update 
    CURRENT_FRAME.frame.destroy()
    CURRENT_FRAME = make_new_frame()
    CURRENT_FRAME.pack()

    # make a frame centered in the middle of the window
    waiting_room_frame = tk.Frame(master=CURRENT_FRAME.frame,width=1,height=1,bg=CONFIG.win_palete[1])
    waiting_room_frame.grid(row=0,column=0)

    # lable saying "waiting for players to start"
    waiting_lable = tk.Label(
        master=waiting_room_frame,
        font=(CONFIG.win_font,20),
        text="Waiting for players to start",
        fg=CONFIG.win_palete[3],
        bg=CONFIG.win_palete[1]
        )
    
    waiting_lable.grid(row=0,column=0)
    
    # loading bar saying "PLAYERS[----    ]"
    current_player_count = tk.Label(
        master=waiting_room_frame,
        font=(CONFIG.win_font,20),
        text="PLAYERS",
        fg=CONFIG.win_palete[3],
        bg=CONFIG.win_palete[1]
        )

    current_player_count.grid(row=1,column=0)

    # wait until game starts , in the mean time update the loading bar.
    while True :
        # get data from the queue
        try :
            data , flag = queue.get_nowait()
        except:
            root.update()
            continue

        if flag == "disp": # if the data is a loading bar update
            current_player_count.config(text=data)

        if flag == "start": # when the game starts update loading bar , write room full and then run mainloop :
            current_player_count.config(text=data)
            waiting_lable.config(text="Room Full")
            root.update()
            break
        root.update()
    main_loop(sock,addr,root,queue)  
# ----------------------------------------------------------------------------------------

# --------------- info input to join server , name and sever addr as well as a submit button ---------------

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
    bg=CONFIG.win_palete[2],
    font=(CONFIG.win_font,18),
    fg=CONFIG.win_palete[0],
    activebackground=CONFIG.win_palete[3],
    command=on_info_submit
    )
submit_button.grid(row=2,column=0,padx=20,pady=20)
global info_submitted
info_submitted = False

def submit_wrapper():
    info_submitted = True
    on_info_submit()



# ----------------------------------------------------------------------------------------
################################ MAIN LOOP ###############################################
# ----------------------------------------------------------------------------------------


# ---- network flags ----

# disp : message send from server to be displayed by client to user
# start : tells clients the game is  starting 
# close : tells client to close connection / this connection is closing (msg half is to be displayed as reason) 
# dispHand : client should display the hand data
# choseCard : tells client to choose a card and send back the card id
# nickname : client sending nickname to server


def main_loop(sock:ntwk.connection,server_addr,root2:tk.Tk,recv_queue:thrd_queue.Queue) :
    global CURRENT_FRAME , root ,TEMP_DISCARD_PILE,TEMP_PLAYER_HAND,TEMP_PLAYERS_HAND_SIZES
    TEMP_PLAYER_HAND = []
    TEMP_DISCARD_PILE = []
    TEMP_PLAYERS_HAND_SIZES = []

    CURRENT_FRAME.frame.destroy()

    #  ------- window setup ----------

    root.minsize(width=900,height=650)
    root.columnconfigure(weight=1,index=0)
    root.rowconfigure(weight=1,index=0)

    # SIDE BAR
    side_bar = tk.Frame(
        master=root,
        bg="yellow",
        width=250

        )
    side_bar.grid(row=0,column=1,sticky=tk.NS)

    # main grid 
    main_grid = tk.Frame(
        master=root,
        bg= "red"
    )
    main_grid.grid(row=0,column=0,sticky=tk.NSEW)
    main_grid.columnconfigure(weight=1,index=0)
    main_grid.rowconfigure(weight=1,index=0)

    # other players 

    players_frame = g_widgets.scrollableFrame(
        main_grid,
        bg="green",
    )
    players_frame.container.grid(row=0,column=0,sticky=tk.NSEW)

    def send_id(id):
        print(id)
        sock.send(id,"chooseCard")

    # deck
    client_deck = g_widgets.hand_gui(
        master=main_grid,
        bg="blue",
        height=200,
        on_click=send_id,
        width=10,
        cards=[]
    )
    client_deck.frame.grid(row=1,column=0,sticky=tk.EW)
    client_deck.disable()

    # pickup card 
    pickupCard = g_widgets.cardButton(
        master=side_bar,
        bg="yellow",
        on_click=send_id,
        name=-1,
        width=164,
        height=256,
        path= root_dir + r'\\assets\\cards\\back.png'
    )
    pickupCard.place(x=50,y=50)

    # discard card 
    discard_card = g_widgets.cardImage(
        master=side_bar,
        bg='yellow',
        path = root_dir + r'\\assets\\cards\\back.png',
        width=164,
        height=256
    )
    discard_card.place(x=50,y=300)

    def get_server_requests():
        global TEMP_DISCARD_PILE,TEMP_PLAYER_HAND,TEMP_PLAYERS_HAND_SIZES
        try: 
            msg , flag = recv_queue.get_nowait()
        except thrd_queue.Empty :
            return

        print("DATA IN :",msg,flag)
        # GAME UPDATE

        if flag == "gameUpdate" :
            try:
                old_cards = [card.ID for card in TEMP_PLAYER_HAND.deck]
            except AttributeError :
                old_cards = []
            # update the temp variables 
            TEMP_PLAYERS_HAND_SIZES = msg[0]
            TEMP_PLAYER_HAND = msg[1]
            TEMP_DISCARD_PILE = msg[2]
            # then display the game
            new_cards = [(root_dir+"\\"+card.asset_path,card.ID) for card in TEMP_PLAYER_HAND.deck]
            new_cards = [card for card in new_cards if card[1] not in old_cards]
            client_deck.add_cards(new_cards)
            discard_card.update_card(root_dir + '\\' +TEMP_DISCARD_PILE.deck[0].asset_path)
            pass


        # CLOSE data = close reason 
        
        elif flag == "close" :
            sock.close()
            print(f"<server> : {msg}")
            return "exit"
            pass
        
        # DISPLAY
        
        elif flag == "disp" :
            print(f"\n{msg}")
        
        # CHOOSE CARD
                
        elif flag == "chooseCard":
            # send message recive to server
            sock.send(f'recived {flag}','confirm')
            # print hand and ask for card choice by id (also check if id is in hand)
            client_deck.enable()
            pickupCard.enable()

        elif flag == "turnend":
            if not msg == -1 : client_deck.remove_card(msg)
            client_deck.disable()
            pickupCard.dissable()
        
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
                    colour[chosen_colour_index]
                except:
                    print("Invalid input, please choose a number from above.")
                    continue
                break
            
            sock.send(chosen_colour_index,"chooseColour")

        else :
            pass

        msg,flag = '',''

    def frame_updates(framerate):

        get_server_requests()
        client_deck.update(framerate)

        pass

    def mainloop():
        frame_rate = CONFIG.framerate
        frame_time = 1/frame_rate
        start_frame = time.time()  
        time_left = lambda: frame_time - (time.time()-start_frame)
        
        # framerate
        fps_counter = tk.Label(text="N/A")
        fps_counter.place(x=0,y=0)

        while True :
            start_frame = time.time()
            frame_updates(frame_rate)
            root.update()
            tleft = time_left()-0.001
            if not (tleft < 0) : 
                time.sleep(tleft)
            fps_counter.config(text=f"fps: {1/(time.time()-start_frame):.2f}")

    mainloop()

while not info_submitted :
    root.update()
    time.sleep(1/CONFIG.framerate)