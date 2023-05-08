import tkinter as tk ,time
import main.lib.game_widgets as g_widgets

root = tk.Tk(sync=True,baseName="TEST")
root.geometry("500x500")
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

for index in range(4):
    tk.Label(text=index,master=players_frame.scrollFrame).pack()


# dumy deck

deck = tk.Frame(
    master=main_grid,
    bg="blue",
    height=200
)

deck.grid(row=1,column=0,sticky=tk.EW)


# -----------------------------------
# framerate manager
# ----------------------------------

def frame_update(framerate):
    pass



def mainloop():
    frame_rate = 60
    frame_time = 1/frame_rate
    start_frame = time.time()  
    time_left = lambda: frame_time - (time.time()-start_frame)
    
    # framerate
    fps_counter = tk.Label(text="N/A")
    fps_counter.place(x=0,y=0)

    while True :
        start_frame = time.time()
        if not (root.focus_displayof() == None) :
            frame_update(frame_rate)
        else:
            time.sleep(1/10)
        root.update()
        if not (time_left() <= 0.001) : 
            time.sleep(time_left()-0.001)
        fps_counter.config(text=f"fps: {1/(time.time()-start_frame):.2f}")

mainloop()
