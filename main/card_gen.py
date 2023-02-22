

from PIL import Image 
import os ,tkinter as tk , threading as thrd ,time

if __name__ != "__main__" :
    import main.lib.loading_bars as loading_bars
    import main.CONFIG as CONFIG
else:
    import lib.loading_bars as loading_bars
    import CONFIG 
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


root = tk.Tk()
root.title("loading")
root.geometry("620x50")

number = 0

loading_bar = loading_bars.win_loadingbar(root,number/len(order),15,"loading card assets",CONFIG.win_font,24,fg=CONFIG.win_palete[3],bg=CONFIG.win_palete[1])
loading_bar.pack()

def gen_cards() :
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
            
            bar = loading_bars.loadingbar(number/len(order),10,"loading card assets")

            loading_bar.config(text=bar)
    time.sleep(0.5)
    root.destroy()
    return

gen_thread = thrd.Thread(target=gen_cards)
gen_thread.start()
root.mainloop()

        

