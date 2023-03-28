import tkinter as tk ,os ,time

root = tk.Tk()
win_width = 265
win_height = 356
root.geometry(f"{win_width}x{win_height}")

root_dir = os.path.dirname(os.path.realpath(__file__))

class card_img():
    def __init__(self,path,master):
        self.path = path
        self.img = tk.PhotoImage(file=path)
        self.canvas = tk.Button(master=master,width=164,height=262,image=self.img,relief="flat",borderwidth=0,fg="white",padx=0,pady=0,overrelief="flat")

    def pack(self,x):
        self.canvas.place(x=x,y=100)

frame = tk.Frame(width= 500 , height= 500 , bg="white",master=root)
frame.pack()
image1 = card_img(r"C:\Users\DanTrinder\Documents\GitHub repositrys\uno-3.0\main\assets\cards\red\+4.png",frame)

image1.pack(100)

image2 = card_img(r"C:\Users\DanTrinder\Documents\GitHub repositrys\uno-3.0\main\assets\cards\red\+4.png",frame)

image2.pack(120)
while True:
    root.update()
    x,y = root.winfo_pointerxy()
    widget = root.winfo_containing(x,y)
    print("widget:", widget)
    time.sleep(1/60)