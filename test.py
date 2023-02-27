import tkinter as tk ,os

root = tk.Tk()
win_width = 265
win_height = 356
root.geometry(f"{win_width}x{win_height}")

root_dir = os.path.dirname(os.path.realpath(__file__))

class entry_box():
    def __init__(self,master,title:str,font,bg,fg,title_color,text_colour,box_width):
        self.frame = tk.Frame(master=master,width=1,height=1,bg=bg)
        self.box = tk.Entry(master=self.frame,fg=text_colour,font=font,bg=fg,width=box_width)
        self.title = tk.Label(master=self.frame,text=title,font=font,fg=title_color,bg=bg)
        self.frame.columnconfigure(index=1,weight=1)
        self.title.grid(column=0,row=0,padx=5,pady=2)
        self.box.grid(column=1,row=0,padx=5,pady=2)
    
    def get_box(self):
        return self.box.get()
    
    def dissable(self):
        self.box.config(state="disabled")


new_box = entry_box(root,"TEST :",("arial",15),"red","blue","orange","white",30)

root.columnconfigure(index=0,weight=1)
new_box.frame.grid(row=0,column=0)
new_box.dissable()

root.mainloop()