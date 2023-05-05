import tkinter as tk 
from PIL import Image , ImageTk

class hand_gui():

    class card_img():
        def __init__(self,path,master,name,on_click,width,height,bg):
            self.path = path
            self.raised = False
            self.name = name
            self.width = int(width)
            self.height = int(height)

            # image stuff

            # open image 
            self.img = Image.open(self.path)
            #resize it
            self.img.thumbnail((self.width,self.height))
            # make it into a tk compatiable image
            self.img = ImageTk.PhotoImage(self.img)
            self.button = tk.Button(
                master=master,
                width=self.width,height=self.height,
                image=self.img,
                command= lambda : on_click(name),
                name=str(name),
                state="normal",
                relief="flat",
                bd=0,
                anchor=tk.NW,
                bg="blue"
                )

        def place(self,**k):
            x,y = k.get("x") , k.get("y")
            if x == None : x = self.button.winfo_x()
            if y == None : y = self.button.winfo_y()
            self.button.place(x=x,y=y)
                
    def __init__(self,cards,on_click,width,height,master,bg):
        self.widgets = []
        self.frame = tk.Frame(width=width,height=height,master=master,bg="red")
        self.funct_out = on_click
        self.width = width
        self.height = height
        self.card_height = (self.height*0.8)
        self.card_width = ((162/254)*self.height*0.8)
        self.max_raise_height = int(self.height*0.2)
        self.bg = bg
        self.add_cards(cards)
        self.draw_cards()
        pass
    
    def raise_card(self,index,framerate):
        card = self.widgets[index]
        current_y = card.button.winfo_y() 
        if current_y == 0 :
            return
        else:
            new_y = current_y - self.max_raise_height/(framerate*0.15)
            if new_y < 0 : new_y = 0
            card.place(y=new_y)

    def lower_card(self,index,framerate):
        card = self.widgets[index]
        current_y = card.button.winfo_y()
        if current_y == self.max_raise_height :
            return
        else:
            new_y = current_y + self.max_raise_height/(framerate*0.15)
            if new_y > self.max_raise_height : new_y = self.max_raise_height
            card.place(y=new_y)

    def set_cards(self,cards:list):
        self.widgets = []
        self.add_cards(cards)

    def add_cards(self,cards:list):
        for card in cards : 
            self.widgets.append(self.card_img(card[0],self.frame,card[1],self.funct_out,self.card_width,self.card_height,self.bg))
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
        
        spacing =(self.width-self.card_width)/(number_of_cards -1)

        if spacing > self.card_width : 
            spacing = self.card_width

        for index,card in enumerate(self.widgets) :
            card.place(x=index*spacing,y=0)

    def update(self,framerate):
        x,y = self.frame.winfo_pointerxy()
        current_widget = self.frame.winfo_containing(x,y)
        for index,widget in enumerate(self.widgets) :
            if current_widget == widget.button :
                self.raise_card(index,framerate)
            else: 
                self.lower_card(index,framerate)
    
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
    path = r"C:\Users\DanTrinder\Documents\GitHub repositrys\uno-3.0\main\assets\cards\green\+2.png"
    cards = [
        (path,1),
        (path,2),
        (path,3),
        (path,4),
        (path,5)
    ]

    # card dims width=164 , height=252

    deck = hand_gui(master=root,cards=cards,on_click=print,width=300,height=300,bg="green")
    deck.frame.pack()

    def frame_update(framerate):
        deck.update(framerate)
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
            if not (time_left() < 0) : 
                time.sleep(time_left())
            fps_counter.config(text=f"fps: {1/(time.time()-start_frame):.2f}")


    mainloop()

        

