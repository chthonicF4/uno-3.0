import tkinter as tk ,os

root = tk.Tk()
win_width = 265
win_height = 356
root.geometry(f"{win_width}x{win_height}")

root_dir = os.path.dirname(os.path.realpath(__file__))


class card_img():
    def __init__(self,path,master):
        self.path = path
        self.canvas = tk.Canvas(master=master,width=166,height=265)
        self.img = tk.PhotoImage(file=path)
        self.canvas.create_image(83,135,image=self.img)

    def pack(self):
        self.canvas.pack()

image = card_img(r"C:\Users\DanTrinder\Documents\GitHub repositrys\uno-3.0\main\assets\cards\red\+4.png",root)

image.pack()

root.mainloop()