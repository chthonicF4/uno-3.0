widgets = []

for index,card in enumerate(cards) :
    widgets.append(card_img(card[0],frame,card[1],when_clikc))
    widgets[index].pack(index*50)