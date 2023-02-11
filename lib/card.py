import random

class card():

    def update(self,colour,type,ID):
        self.colour = colour
        self.type = type
        self.ID = ID
        self.name = f"{self.colour} {self.type}"
        self.disp_name = f"{self.name:<11} : {self.ID}"

    def __init__(self,colour,type,ID):
        self.update(colour,type,ID)
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
        return "coljasdasd"
        pass


    def add(self,card):
        self.deck.insert(0,card)

    def take(self,index=0) :
        return self.deck.pop(index)
    
    def print(self):
        for index , card in enumerate(self.deck) :
            print(f"[{index:^2}] : {card.disp_name}")
