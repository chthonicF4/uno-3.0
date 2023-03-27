
import math , pickle

def string_deconstruct(size:int,str:str):
    out = []
    for x in range(math.floor(len(str)/size)):
        out.append(str[0:size])
        str = str[size:]
    out.append(str)
    return out

str = b""
data = None

for x in string_deconstruct(3,pickle.dumps("hello")) :
    str += x 
    try : data = pickle.loads(str)
    except:
        pass
    print(data)


