import tkinter as tk ,os

root = tk.Tk()
win_width = 265
win_height = 356
root.geometry(f"{win_width}x{win_height}")

root_dir = os.path.dirname(os.path.realpath(__file__))

canvas = tk.Canvas(master=root,width=win_width,height=win_height)
img = tk.PhotoImage(file=f"{root_dir}\\main\\assets\\cards\\black\\+4.png")
canvas.create_image(win_width//2,win_height//2,image = img)
canvas.pack()


root.mainloop()