from time import sleep
ON = True
escp = "\033["

def Crmv(string):
    index = string.find(escp)
    while index != -1 :
        # find end of thing
        end = index
        char = 0
        while char != "m" :
            char = string[end]
            end += 1
        string = string.replace(string[index:end],"")
        index = string.find(escp)
    return string

def c(string,**kwargs) :
    if ON != True :
        return string
    fgc = kwargs.get("fg",None)
    bgc = kwargs.get("bg",None)
    utc = kwargs.get("ut",None)
    cps = kwargs.get("cps",None)
    reset = kwargs.get("reset",True)
    code = ""
    if cps :
        if cps.fg :
            code += f"{escp}{fg[cps.fg]}" 
        if cps.bg :
            code += f"{escp}{bg[cps.bg]}" 
        if cps.ut :
            if type(cps.ut) is str :
                utp = [cps.ut]
            else:
                utp = cps.ut
            for cd in utp :
                code += f"{escp}{ut[cd]}"
    if fgc :
        code += f"{escp}{fg[fgc]}"
    if bgc :
        code += f"{escp}{bg[bgc]}"
    if utc :
        if type(utc) is str :
            utc = [utc]
        for cd in utc :
            code += f"{escp}{ut[cd]}"
    if reset == True :
        return f"{code}{string}{escp}\033[0m"
    else :
        return f"{code}{string}{escp}"

ut = {
    "reset": '0m',
    "bold": '01m',
    "disable": '02m',
    "underline": '04m',
    "reverse": '07m',
    "strikethrough": '09m',
    "invisible": '08m',
}
fg = {
    "black": '30m',
    "red": '31m',
    "green": '32m',
    "orange": '33m',
    "blue": '34m',
    "purple": '35m',
    "cyan": '36m',
    "lightgrey": '37m',
    "darkgrey": '90m',
    "lightred": '91m',
    "lightgreen": '92m',
    "yellow": '93m',
    "lightblue": '94m',
    "pink": '95m',
    "lightcyan": '96m',
}
bg = {
    "black": '40m',
    "red": '41m',
    "green": '42m',
    "orange": '43m',
    "blue": '44m',
    "purple": '45m',
    "cyan": '46m',
    "lightgrey": '47m',
}
if __name__ == "__main__" :
    print("preparing to print")
    sleep(1)
    #ut 
    print("\n UT :\n")
    for x in ut :
        print(f"{x} , {ut[x]} : {escp}{ut[x]} test {escp}0m")
    #fg
    print( "\n FG :\n")
    for x in fg :
        print(f"{x} , {fg[x]} : {escp}{fg[x]} test {escp}0m")
    #bg
    print( "\n BG :\n")
    for x in bg :
        print(f"{x} , {bg[x]} : {escp}{bg[x]} test {escp}0m")
    input("press enter to exit")
class colrP :
    def __init__(self,**kwargs) -> None:
        self.fg = kwargs.get("fg",None)
        self.bg = kwargs.get("bg",None)
        self.ut = kwargs.get("ut",None)
        pass