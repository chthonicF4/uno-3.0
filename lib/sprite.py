import math
from tkinter import *
class sprite :
    def __init__(self,x,y,direction = 0):
        self.x = x
        self.y = y
        self.x_exact = float(x)
        self.y_exact = float(y)
        self.direction = direction

    
    def move (self,distance) :
        deg2rad = (2*math.pi)/360
        if self.direction == 0 or self.direction == 360:
            self.x_exact += distance
        elif 0 < self.direction < 90 :
            self.x_exact += distance*(math.cos(self.direction*deg2rad))
            self.y_exact += distance*(math.sin(self.direction*deg2rad))
        elif self.direction == 90 :
            self.y_exact += distance
        elif 90 < self.direction < 180 :
            self.x_exact += 0 - distance*(math.cos((180-self.direction)*deg2rad))
            self.y_exact += distance*(math.sin((180-self.direction)*deg2rad))
        elif self.direction == 180 :
            self.x_exact += 0 - distance
        elif 180 < self.direction < 270 :
            self.x_exact += 0 - distance*(math.cos((self.direction - 180)*deg2rad))
            self.y_exact += 0 - distance*(math.sin((self.direction - 180)*deg2rad))
        elif self.direction == 270 :
            self.y_exact += 0 - distance
        else :
            self.x_exact += distance*(math.cos((360 - self.direction)*deg2rad))
            self.y_exact += 0 - distance*(math.sin((360 - self.direction)*deg2rad))            
        self.x = round(self.x_exact)
        self.y = round(self.y_exact)
        self.update()
    
    def change_x(self,ammount) :
        self.x_exact += ammount
        self.x = round(self.x_exact)
        self.update()
    
    def change_y(self,ammount) :
        self.y_exact += ammount
        self.y = round(self.y_exact)
        self.update()

    def set_x(self,ammount) :
        self.x_exact = ammount
        self.x = round(self.x_exact)
        self.update()
    
    def set_y(self,ammount) :
        self.y_exact = ammount
        self.y = round(self.x_exact)
        self.update()
    
    def go_to(self,x,y) :
        self.x_exact = x
        self.y_exact = y
        self.x = round(self.x_exact)
        self.y = round(self.y_exact)
        self.update()

    def turn(self,direction,ammount):
        if direction == "l" :
            self.direction += 0 - ammount
        elif direction == "r" :
            self.direction += ammount
        else :
            print("error:",ammount,"is not 'l' or 'r' ")
        self.update()
    
    def touching(self,other) :
        if other.x == self.x and other.y == self.y :
            return True 
        else :
            return False
        
    def set_direction(self,direction):
        self.direction = direction
        self.update()

    def update(self) :
        pass

    def clone(self) :
        clone = sprite(self.x,self.y,direction = int(self.direction))
        return clone