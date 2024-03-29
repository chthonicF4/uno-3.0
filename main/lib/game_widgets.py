import tkinter as tk 
from tkinter import ttk
from PIL import Image , ImageTk

class cardButton():
    def __init__(self,path,master,name,on_click,width,height,bg):
        self.path = path
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
            #name=str(name),
            state="normal",
            relief="flat",
            bd=0,
            anchor=tk.NW,
            bg=bg
            )   

    def place(self,**k):
        x = k.get("x")
        y = k.get("y")
        self.button.place(x=x,y=y)

    def resize(self,new_width,new_height):
        self.width = int(new_width)
        self.height = int(new_height)
        self.img = Image.open(self.path)
        self.img.thumbnail((self.width,self.height))
        self.img = ImageTk.PhotoImage(self.img)
        self.button.config(width=self.width,height=self.height,image=self.img)
    
    def enable(self):
        self.button['state'] = tk.NORMAL

    def dissable(self) :
        self.button['state'] = tk.DISABLED

class hand_gui():
                
    def __init__(self,cards,on_click,width,height,master,bg):
        self.widgets = []
        self.frame = tk.Frame(width=width,height=height,master=master,bg=bg)
        self.funct_out = on_click
        self.enabled = True
        self.width = width
        self.height = height
        self.card_height = (self.height*0.8)
        self.card_width = ((162/254)*self.height*0.8)
        self.max_raise_height = int(self.height*0.2)
        self.bg = bg
        self.add_cards(cards)
        self.draw_cards()
        self.frame.bind("<Configure>", self.calculate_proportions)
        pass

    def calculate_proportions(self,event):
        if not(event.widget == self.frame) :
            return
        self.width = event.width
        self.height = event.height
        self.card_height = (self.height*0.8)
        self.card_width = ((162/254)*self.height*0.8)
        self.max_raise_height = int(self.height*0.2)

        for card in self.widgets :
            card.resize(self.card_width,self.card_height)

        self.draw_cards()
    
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
        for card in self.widgets :
            card.button.destroy()
        self.widgets = []
        self.add_cards(cards)

    def add_cards(self,cards:list):
        for card in cards : 
            self.widgets.append(cardButton(card[0],self.frame,card[1],self.funct_out,self.card_width,self.card_height,self.bg))
        self.draw_cards()
        if self.enabled == True : self.enable()
        else : self.disable()
    
    def remove_card(self,name):
        for index , card in enumerate(self.widgets) :
            if card.name == name :
                self.widgets.pop(index).button.destroy()
                break
        self.draw_cards()
    
    def draw_cards(self):
        number_of_cards = len(self.widgets)

        # resize cards 


        if number_of_cards == 0:
            return
        if number_of_cards == 1 :
            self.widgets[0].place(x=(self.width -self.card_width)//2)
            return

        
        spacing =(self.width-self.card_width)/(number_of_cards -1)
        offset = 0

        if spacing > self.card_width : 
            spacing = self.card_width
            offset = (self.width - self.card_width*number_of_cards)//2

        for index,card in enumerate(self.widgets) :
            card.place(x=(index*spacing + offset))

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
        self.enabled = True

    def disable(self):
        for widget in self.widgets :
            widget.button['state'] = tk.DISABLED
        self.enabled = False

class scrollableFrame():
    def __init__(self,master,bg):
        self.container = tk.Frame(
            master=master,
            bg=bg
        )
        self.canvas = tk.Canvas(
            master=self.container,
            bg=bg,
            highlightthickness=0
        )
        self.scrollBar = tk.Scrollbar(
            master=self.container,
            troughcolor=bg,
            orient="vertical",
            command=self.canvas.yview
        )
        self.scrollFrame = tk.Frame(
            master=self.canvas,
            bg=bg
        )
        self.scrollFrame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(
                scrollregion=self.canvas.bbox("all")
            )
        )
        self.scrollFrameID = self.canvas.create_window(
            (0,0),
            anchor="nw",
            window=self.scrollFrame,
        )
        self.canvas.configure(yscrollcommand=self.scrollBar.set)
        self.canvas.pack(side="left",fill="both",expand=True)
        self.canvas.bind("<Configure>", self.resize_frame)
        self.scrollBar.pack(side="right",fill="y")
    
    def resize_frame(self,e):
        self.canvas.itemconfig(self.scrollFrameID, width=e.width)

class cardImage():
    def __init__(self,master,bg,path,width,height):

        self.width = int(width)
        self.height = int(height)

        self.make_image(path)

        self.lable = tk.Label(
            master=master,
            bg=bg,
            image= self.img,
            width=self.width,
            height=self.height,
            highlightthickness=0,
            bd=0
        )
        pass

    def make_image(self,path):
        self.path = path
        # open image 
        self.img = Image.open(self.path)
        #resize it
        self.img.thumbnail((self.width,self.height))
        # make it into a tk compatiable image
        self.img = ImageTk.PhotoImage(self.img)
    
    def place(self,**k):
        x = k.get('x')
        y = k.get('y')
        self.lable.place(x=x,y=y)

    def update_card(self,path):
        self.make_image(path)
        self.lable.configure(image=self.img)
        
class playerHand():

    def __init__(self,master,seporatorColour,bg,textColour,index:int,name:str,count:int,font:str,path:str):
        self.path = path
        self.bg = bg
        self.numb = count
        self.container = tk.Frame(
            master=master,
            bg=bg,
            highlightcolor=seporatorColour,
            highlightthickness=2
        )
        self.container.columnconfigure(index=1,weight=1)
        self.nameFrame = tk.Frame(
            master=self.container,
            bg=bg
        )
        self.nameFrame.grid(row=0,column=0)
        self.indexLable = tk.Label(
            master=self.nameFrame,
            bg=bg,
            text=f'P{index} :',
            font=(font,14),
            fg=textColour
            )
        self.nameLable = tk.Label(
            master=self.nameFrame,
            bg=bg,
            text=f'{name}',
            font=(font,14),
            fg=textColour
            )
        self.handFrame = tk.Frame(
            master=self.container,
            bg=bg,
            height=75

        )
        self.handFrame.grid(row=0,column=1,sticky='NSEW',padx=10,pady=10)

        self.setNumber(numb=count)

        self.handFrame.bind("<Configure>", self.resize)
        
        self.indexLable.pack(anchor=tk.W)
        self.nameLable.pack()

    def drawCards(self):
        numbCards = len(self.cardWidgets)
        if numbCards == 0 :
            return
        if numbCards == 1 :
            self.cardWidgets[0].place(x=(self.width-self.cardWidth)/2,y=0)
            return
        spacing = (self.width-self.cardWidth)/(numbCards -1)
        if spacing > self.cardWidth :
            offset = (self.width-(self.cardWidth*numbCards))/2
            spacing = self.cardWidth
        else : offset = 0
        for index,card in enumerate(self.cardWidgets):
            card.place(x=(index*spacing + offset),y=0)
            
        
    def calculateDims(self,*k):
        if len(k)>0 :
            self.width = k[0].width
            if self.height == k[0].height :
                return True
            else:
                self.height = k[0].height
        else:
            self.height = 20
            self.width = 20
        self.cardWidth = (162/254)*self.height

    def resize(self,event):
        if not self.calculateDims(event):
            self.cardWidgets = [cardImage(
                master=self.handFrame,
                bg=self.bg,
                path=self.path,
                width=self.cardWidth,
                height=self.height
                ) for number in range(self.numb)]
        self.drawCards()

        

    def setNumber(self,numb):
        self.numb = numb
        self.calculateDims()
        self.cardWidgets = [cardImage(
            master=self.handFrame,
            bg=self.bg,
            path=self.path,
            width=self.cardWidth,
            height=self.height
            ) for number in range(numb)]
        self.drawCards()
        pass



if __name__ == "__main__" :
    import time
    root = tk.Tk()
    root.geometry("500x500")
    root.columnconfigure(weight=1,index=0)
    root.rowconfigure(weight=1,index=0)

    cool = scrollableFrame(master=root,bg='green')

    dingus = [playerHand(
        master=cool.scrollFrame,
        bg='white',
        textColour='black',
        seporatorColour = 'grey',
        index=numb,
        name='SHOBON',
        count=numb,
        font='helvetica',
        path=r"C:\Users\DanTrinder\Documents\GitHub repositrys\uno-3.0\main\assets\cards\back.png"
    ) for numb in range(8)]

    cool.scrollFrame.columnconfigure(index=0,weight=1)

    for index , thing in enumerate(dingus) :
        thing.container.grid(row=index,column=0,sticky='EW')

    cool.container.grid(row=0,column=0,sticky=tk.NSEW)

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


        

 