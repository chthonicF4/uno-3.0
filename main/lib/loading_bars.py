import tkinter as tk

def loadingbar(value:float,length:int,name:str):
    squares = value*length
    bar = ""
    for unit in range(length):
        if unit < (squares) : bar += "■"
        else: bar += " "
    return f"{name} [{bar}]"


def win_loadingbar(master,value:float,length:int,name:str,font:str,size:int,fg:str,bg:str):
    text = loadingbar(value,length,name)
    lable = tk.Label(master=master,text=text,font=(font,size),fg=fg,bg=bg)
    return lable






