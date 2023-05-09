import tkinter as tk ,time
import main.lib.game_widgets as g_widgets

root = tk.Tk(sync=True,baseName="TEST")
root.geometry("500x500")
root.minsize(width=900,height=650)

root.columnconfigure(weight=1,index=0)
root.rowconfigure(weight=1,index=0)



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
