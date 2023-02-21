from PIL import Image
import os
card_width = 165
card_height = 256

card_grid_width = 12
card_grid_height = 6

card_x_pad = 2.5
card_y_pad = 2.5

root_dir = os.path.dirname(os.path.realpath(__file__))

root_image = Image.open(f"{root_dir}\\assets\\all_cards.png")

directorys_to_make = [
    "assets\\cards",
    "assets\\cards\\red",
    "assets\\cards\\blue",
    "assets\\cards\\yellow",
    "assets\\cards\\green",
    "assets\\cards\\black"
    ]

for dir in directorys_to_make:
    try:
        os.mkdir(os.path.join(root_dir,dir))
    except:
        pass


order = [    
    "back",
    "black\\wild",
    "yellow\\wild",
    "red\\wild",
    "blue\\wild",
    "green\\wild",
    "black\\+4",
    "yellow\\+4",
    "red\\+4",
    "blue\\+4",
    "green\\+4",
    None,
    ]

for colour in ["yellow","red","blue","green"] :

    for number in range(1,10):
        order.append(f"{colour}\\{number}")
    order += [ 
        f"{colour}\\0",
        f"{colour}\\+2",
        f"{colour}\\skip",
        f"{colour}\\reverse"
    ]

order += [None]*8

for grid_y in range(0,card_grid_height):
    for grid_x in range(0,card_grid_width):
        number = grid_y*card_grid_width + grid_x
        if order[number] == None :
            continue

        left = grid_x*(card_width+card_x_pad)
        right = left + card_width
        top = grid_y*(card_height+card_y_pad)
        bottom = top + card_height

        card = root_image.crop((left,top,right,bottom))
        new_image_path = f"assets\\cards\\{order[number]}.png"
        card.save(os.path.join(root_dir,new_image_path))
        

