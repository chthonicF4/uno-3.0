import tkinter as tk 
from PIL import Image , ImageTk

class hand_gui():

    class card_img():
        def __init__(self,path,master,name,on_click,width,height,y,bg):
            self.path = path
            self.raised = False
            self.name = name
            
            self.const_y = y
            self.y = y
            self.width = width
            self.height = height

            # image stuff

            # open image 
            self.img = Image.open(self.path)
            #resize it
            self.img.thumbnail((self.width,self.height))
            # make it into a tk compatiable image
            self.img = ImageTk.PhotoImage(self.img)
            self.button = tk.Button(
                master=master,
                width=164,height=252,
                image=self.img,
                command= lambda : on_click(name),
                name=str(name),
                state="normal",
                relief="flat",
                bd=0,
                anchor=tk.NW,
                bg=bg
                )

        def place(self,**k):
            x,y = k.get("x") , k.get("y")
            self.button.place(x=x,y=y)
                
    def __init__(self,cards,on_click,width,height,master,bg):
        self.widgets = []
        self.frame = tk.Frame(width=width,height=height,master=master,bg="red")
        self.funct_out = on_click
        self.width = width
        self.height = height
        self.card_width ,self.card_height = 164 , 252
        self.add_cards(cards)
        self.draw_cards()
        self.max_raise_height = 60
        pass
    
    def raise_card(self,index):
        card = self.widgets[index]
        current_y = card.button.winfo_y() - self.card_height
        if current_y == self.max_raise_height :
            return
        else:
            new_y = current_y + self.max_raise_height/10
            if new_y > self.max_raise_height : new_y = self.max_raise_height
            card.place(y=new_y)

    def lower_card(self,index):
        card = self.widgets[index]
        current_y = card.button.winfo_y()
        if current_y == self.max_raise_height :
            return

    def set_cards(self,cards:list):
        self.widgets = []
        self.add_cards(cards)

    def add_cards(self,cards:list):
        for card in cards : 
            self.widgets.append(self.card_img(card[0],self.frame,card[1],self.funct_out,self.card_width,self.card_height,self.card_y,self.bg))
        self.draw_cards()
    
    def remove_card(self,name):
        for index , card in enumerate(self.widgets) :
            if card.name == name :
                self.widgets.pop(index).button.destroy()
                break
        self.draw_cards()
    
    def draw_cards(self):
        number_of_cards = len(self.widgets)

        if number_of_cards == 0:
            return
        
        spacing = self.width / number_of_cards

        if spacing > self.card_width : 
            spacing = self.card_width

        for index,card in enumerate(self.widgets) :
            card.place(x=index*spacing,y=0)

    def update(self):
        x,y = self.frame.winfo_pointerxy()
        current_widget = self.frame.winfo_containing(x,y)
        for widget in self.widgets :
            if current_widget == widget.button :
                print(widget.button.winfo_y(),widget.button.winfo_x())
            else: 
                
                pass#print(widget.button.winfo_y())
    
    def enable(self):
        for widget in self.widgets :
            widget.button['state'] = tk.NORMAL

    def disable(self):
        for widget in self.widgets :
            widget.button['state'] = tk.DISABLED

if __name__ == "__main__" :
    import time
    root = tk.Tk()
    root.geometry("500x500")
    path = r"C:\Users\dan\OneDrive\Documents\GitHub\uno 3.0\main\assets\cards\black\wild.png"
    cards = [
        (path,1),
        (path,2),
        (path,3),
        (path,4),
        (path,5)
    ]

    # card dims width=164 , height=252

    deck = hand_gui(master=root,cards=cards,on_click=print,width=200,height=152)
    deck.frame.pack()

    framerate = 60
    frame_time = 1/framerate
    time_since = lambda start : time.time() - start
    while True :
        start_frame = time.time()
        deck.update()
        root.update()
        total_frame_time = time_since(start_frame)
        delay = frame_time - total_frame_time
        if delay < 0 : delay = 0
        time.sleep(delay)
        print(f"framerate : {1/(time.time()-start_frame):.04}",end="\r")

        

