import tkinter as tk , main.CONFIG as CONFIG , time

global stop ,choice
stop = False
choice = ""

def join(**k):
    global stop ,choice
    stop = True
    choice = "client"

def host(**k):
    global stop ,choice
    stop = True
    choice = "server"



win_font = CONFIG.win_font
win_palete = CONFIG.win_palete

win_width = CONFIG.win_width
win_height = CONFIG.win_height
title = CONFIG.win_title

root = tk.Tk()
root.geometry(f"{win_width}x{win_height}")
root.title(title)
root.config(bg=win_palete[1])

# title frame 

frame  = tk.Frame(master=root,width=win_width,height=win_height,bg=win_palete[1])
root.columnconfigure(index=0,weight=1)
root.rowconfigure(index=0,weight=1)
frame.grid()

# title 

title_lable = tk.Label(master=frame,text="UNO 3.0",font=(win_font,24),fg=win_palete[3],bg=win_palete[1])
title_lable.pack()

# button spacing 
padding = 5

# client button

client_button = tk.Button(master=frame,command=join,width=20,height=2,text="join",bg=win_palete[2],font=(win_font,18),fg=win_palete[0],activebackground=win_palete[3])
client_button.pack(padx=padding,pady=padding)

# host button

host_button = tk.Button(master=frame,command=host,width=20,height=2,text="host",bg=win_palete[2],font=(win_font,18),fg=win_palete[0],activebackground=win_palete[3])
host_button.pack(padx=padding,pady=padding)


while stop != True :
    root.update()
    time.sleep(1/CONFIG.framerate)
root.destroy()
if choice == "client":
    import main.client
elif choice == "server":
    import main.server




