import random

class card():

    def update(self,**k):
        self.colour = k.get("colour",self.colour)
        self.type = k.get("type",self.type)
        self.ID = k.get("ID",self.ID)
        self.name = f"{self.colour} {self.type}"
        self.asset_path = f"assets\\cards\\{self.colour}\\{self.type}.png"
        self.disp_name = f"{self.name:<11} : {self.ID:<3} {self.asset_path}"

    def __init__(self,colour,type,ID):
        self.colour = colour
        self.type = type 
        self.ID = ID
        self.name = f"{self.colour} {self.type}"
        self.asset_path = f"assets\\cards\\{self.colour}\\{self.type}.png"
        self.disp_name = f"{self.name:<11} : {self.ID:<3} {self.asset_path}"
        pass

class deck():

    def __init__(self):
        self.deck = []
        pass

    def shuffle(self):
        random.shuffle(self.deck)

    def display(self):
        for card in self.deck :
            print(card.disp_name)
    
    def sort(self):

        for index in range(len(self.deck)-1):
            index += 1
            current_card = index
            if self.deck[index-1].ID > self.deck[current_card].ID :
                while self.deck[index-1].ID > self.deck[current_card].ID :
                    index += -1
                    if index == -1 :
                        index = 0
                        break
                self.deck.insert(index,self.deck.pop(current_card))
        pass

    def find_by_id(self,ID): # reutrns an index
        for index , card in enumerate(self.deck) :
            if card.ID == ID :
                return index
        return None


    def add(self,card):
        self.deck.insert(0,card)

    def take(self,index=0) :
        return self.deck.pop(index)
    
    def print(self):
        for index , card in enumerate(self.deck) :
            print(f"[{index:^2}] : {card.disp_name}")
