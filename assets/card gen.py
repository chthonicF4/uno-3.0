from PIL import Image

card_width = 86.3333333333
card_height = 129

card_grid_width = 14
card_grid_height = 8

root_image = Image.open("C:\\Users\\dan\\OneDrive\\Documents\\GitHub\\uno 3.0\\assets\\all_cards.png")


for grid_y in range(0,card_grid_height):
    for grid_x in range(0,card_grid_width):



        card = root_image.crop((grid_x*(card_width-1),grid_y*(card_height-1),(grid_x+1)*(card_width-1)+1 ,(grid_y+1)*(card_height-1)+1))
        number = grid_y*card_grid_width + grid_x
        card.save(f"assets\\cards\\crop_{number}.png")