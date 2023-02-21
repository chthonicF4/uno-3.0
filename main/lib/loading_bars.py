
def loadingbar(value:float,length:int,name:str):
    squares = value*length
    bar = ""
    for unit in range(length):
        if unit < (squares) : bar += "■"
        else: bar += " "
    return f"{name} [{bar}]"
