import tkinter as tk ,os ,time ,threading as thrd

root = tk.Tk()
win_width = 265
win_height = 356
root.geometry(f"{win_width}x{win_height}")

root_dir = os.path.dirname(os.path.realpath(__file__))



def when_clikc(id):
    print(id)

path = root_dir + r"\main\assets\cards\red\+4.png"

cards = [
    (path,1),
    (path,2),
    (path,3),
    (path,4),
    (path,5),
    (path,6),
    (path,7)

]

class hand_gui():

    class card_img():
        def __init__(self,path,master,name,on_click):
            self.path = path
            self.raised = False
            self.y = 60
            self.img = tk.PhotoImage(file=path)
            self.button = tk.Button(
                master=master,
                width=164,height=252,
                image=self.img,
                command= lambda : on_click(name),
                name=str(name),
                state="normal",
                relief="flat",
                fg="white",
                bd=0,
                anchor=tk.NE,
                disabledforeground="red"
                )

        def pack(self,x):
            self.button.place(x=x,y=60)

        def card_raise(self):
            if self.y == 0 :
                return
            else: self.y -= 10 
            self.button.place(y=self.y)
        
        def card_lower(self):
            if self.y == 60 :
                return
            else: self.y += 10
            self.button.place(y=self.y)
                
        


    def __init__(self,cards,on_click,width):
        self.widgets = []
        self.frame = tk.Frame(width=width,height=312)
        self.frame.pack()
        for index,card in enumerate(cards) :
            self.widgets.append(self.card_img(card[0],self.frame,card[1],on_click))
            self.widgets[index].pack(index*50)
        pass
    
    def update(self):
        x,y = self.frame.winfo_pointerxy()
        current_widget = self.frame.winfo_containing(x,y)
        for widget in self.widgets :
            if current_widget == widget.button :
                widget.card_raise()
            else: 
                widget.card_lower()
    
    def enable(self):
        for widget in self.widgets :
            widget.button['state'] = tk.NORMAL

    def disable(self):
        for widget in self.widgets :
            widget.button['state'] = tk.DISABLED


thiong = hand_gui(cards=cards,on_click=when_clikc,width=500)




framerate = 60

while True:
    start_frame = time.time()

    # show what the mouse over  
      
    thiong.update()
    root.update()
        
    
    
    total_frame_time = time.time()-start_frame
    delay  = (1/framerate)-total_frame_time
    if delay < 0 : continue
    time.sleep(delay)