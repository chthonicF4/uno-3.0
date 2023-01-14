
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


# ------- inital clients conecting ----------

sock , server_addr = connect_to_a_server()

# wait unill recive "start" flag
print(f"\nWaiting for players to start :")
data = "ee"
while True:
    data = sock.recv()
    if data[1] == "start" : break
    print(data[0],end="")
    
print(colrs.c(data[0],cps=C_info))

# ------- start game ---------------

hand,flag = sock.recv()
hand.display()