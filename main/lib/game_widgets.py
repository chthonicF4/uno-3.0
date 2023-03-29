import tkinter as tk ,
from PIL import Image

class hand_gui():

    class card_img():
        def __init__(self,path,master,name,on_click,height):
            self.path = path
            self.raised = False
            self.y = height*(60/252)
            self.name = name
            self.img = tk.PhotoImage(file=self.path)
            self.button = tk.Button(
                master=master,
                width=height*(164/252),height=height,
                image=self.img,
                command= lambda : on_click(name),
                name=str(name),
                state="normal",
                relief="flat",
                bd=0,
                anchor=tk.NE
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
                
    def __init__(self,cards,on_click,width,height,master):
        self.widgets = []
        self.frame = tk.Frame(width=width,height=height,master=master)
        self.funct_out = on_click
        self.width = width
        self.height = height
        self.add_cards(cards)
        self.draw_cards()
        pass

    def set_cards(self,cards:list):
        self.widgets = []
        self.add_cards(cards)

    def add_cards(self,cards:list):
        for card in cards : 
            self.widgets.append(self.card_img(card[0],self.frame,card[1],self.funct_out,self.height))
        self.draw_cards()
    
    def remove_card(self,name):
        for index , card in enumerate(self.widgets) :
            if card.name == name :
                self.widgets.pop(index).button.destroy()
                break
        self.draw_cards()
    
    def draw_cards(self):
        card_width , card_height = 164,252

        if len(self.widgets) == 0:
            return
        card_spacing = (self.width-card_width)/len(self.widgets)
        card_offset = (self.width-(len(self.widgets)*card_width))/2
        if card_offset < 0 : card_offset = 0
        if card_spacing >card_width : card_spacing = card_width
        for index , card in enumerate(self.widgets):
            card.pack((index*card_spacing)+card_offset)

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

if __name__ == "__main__" :
    root = tk.Tk()
    root.geometry("500x500")
    path = r"C:\Users\DanTrinder\Documents\GitHub repositrys\uno-3.0\main\assets\cards\red\wild.png"
    cards = [
        (path,1),
        (path,2),
        (path,3)
    ]

    # card dims width=164 , height=252

    deck = hand_gui(master=root,cards=cards,on_click=print,width=500,height=252)
    deck.frame.pack()

    while True :
        deck.update()
        root.update()
        

