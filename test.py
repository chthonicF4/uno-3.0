import tkinter as tk 

class hand_gui():

    class card_img():
        def __init__(self,path,master,name,on_click):
            self.path = path
            self.raised = False
            self.y = 60
            self.name = name
            self.img = tk.PhotoImage(file=path)
            self.button = tk.Button(
                master=master,
                width=164,height=252,
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
                
    def __init__(self,cards,on_click,width):
        self.widgets = []
        self.frame = tk.Frame(width=width,height=312)
        self.frame.pack()
        self.funct_out = on_click
        self.width = width
        for card in cards :
            self.add_card(card)
        self.draw_cards()
        pass
    
    def add_card(self,card:tuple):
        self.widgets.append(self.card_img(card[0],self.frame,card[1],self.funct_out))
        self.draw_cards()
    
    def remove_card(self,name):
        for index , card in enumerate(self.widgets) :
            if card.name == name :
                self.widgets.pop(index).button.destroy()
                break
        self.draw_cards()
    
    def draw_cards(self):
        if len(self.widgets) == 0:
            return
        card_spacing = (self.width-164)/len(self.widgets)
        card_offset = (self.width-(len(self.widgets)*164))/2
        if card_offset < 0 : card_offset = 0
        if card_spacing >164 : card_spacing = 164
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

