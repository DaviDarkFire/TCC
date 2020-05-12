import tkinter as tk
from PIL import ImageTk, Image
import os

def proxima(n):
    print(n)
    global label
    global bt_anterior
    global bt_proxima

    label.grid_forget()
    label = tk.Label(image=img_list[n-1], height=400, width=600)
    bt_proxima = tk.Button(img_window, text=">>", command=lambda: proxima(n+1))
    bt_anterior = tk.Button(img_window, text="<<", command=lambda: anterior(n-1))

    if(n == len(img_list)):
        bt_proxima = tk.Button(img_window, text=">>", state=tk.DISABLED)
    
    label.grid(row=0,column=0,columnspan=2)
    bt_anterior.grid(row=1,column=0)
    bt_proxima.grid(row=1,column=1)

def anterior(n):
    global label
    global bt_anterior
    global bt_proxima

    label.grid_forget()
    label = tk.Label(image=img_list[n-1], height=400, width=600)
    bt_proxima = tk.Button(img_window, text=">>", command=lambda: proxima(n+1))
    bt_anterior = tk.Button(img_window, text="<<", command=lambda: anterior(n-1))

    if(n == 1):
        bt_anterior = tk.Button(img_window, text="<<", state=tk.DISABLED)

    label.grid(row=0,column=0,columnspan=2)
    bt_anterior.grid(row=1,column=0)
    bt_proxima.grid(row=1,column=1)


def create_window(root):
    print("PENES")
    img_window = root
    img_window.title("Imagens Geradas")
    img_extensions = ('.jpg','.jpeg','.JPG','.JPEG','.PNG','.BMP')
    img_list = []
    for img_name in os.listdir("exit/"):
        if(img_name.endswith(img_extensions)):
            img_list.append(ImageTk.PhotoImage(Image.open(f"exit/{img_name}")))

    label = tk.Label(image=img_list[1], height=400, width=600)
    label.grid(row=0,column=0,columnspan=2)

    bt_anterior = tk.Button(img_window, text="<<", command=anterior, state=tk.DISABLED)
    bt_proxima = tk.Button(img_window, text=">>", command=lambda: proxima(3))
    bt_anterior.grid(row=1,column=0)
    bt_proxima.grid(row=1,column=1)


    img_window.mainloop()