import tkinter as tk
import face_identification as face_id
from tkinter import filedialog
import os

PATH = " "

def identify():
    if(PATH != " "):
        face_id.recog_faces(PATH,boundingbox_flag.get())
        f = open("predictions.txt","r") 
        buff = f.read()
        show_text(buff)
    else:
        show_text("Selecione algum diretório.")

def abrir():
    global PATH 
    PATH = filedialog.askdirectory(parent=frame2,title='Escolha uma pasta com fotos e/ou vídeos')
    show_files(PATH)

def show_text(buffer):
    w.delete("all")
    w.create_text(20, 20, anchor='nw' , text=buffer)

def update_facebank():
    show_text("Atualizando encodings...")
    face_id.generate_encodings_from_facebank()
    show_text("Encodings salvos em: \n face_encodings\encodings")

def show_files(path):
    w.delete("all")
    img_folder = path.split('/')[-1]
    strings = f"C:/.../{img_folder}\n"
    i = 20
    for file in os.listdir(path):
        strings += f"{file}\n"
        i += 20
    w.create_text(20, 20, anchor='nw' , text=strings) #n, ne, e, se, s, sw, w, nw
    
###################################################Criação base da janela
window = tk.Tk()
window.title("Face Identification")  # to define the title

canvas = tk.Canvas(window, width=600, height=400)  # define the size
canvas.pack()

frame = tk.Frame(window)
frame.place(relx=0.05, rely=0.05,relwidth=0.45, relheight=0.9)

frame2 = tk.Frame(window)
frame2.place(relx=0.5, rely=0.05,relwidth=0.45, relheight=0.9)

frame3 = tk.Frame(frame, highlightbackground="black", highlightthickness=1)
frame3.place(relx=0.1, rely=0.1,relwidth=0.8, relheight=0.8)

frame4 = tk.Frame(frame2)
frame4.place(relx=-0.04, rely=0.66,relwidth=1, relheight=0.1)

w = tk.Canvas(frame3, width=600, height=600)
w.pack()
label = tk.Label(frame,text='Mídia\Diretório', bd='3', fg='blue', font='Helvetica 9 bold')  # placing labels
label.place(relx=0.0, rely=0.0, relwidth=0.5, relheight=0.05)
##################################################Criação de widgets
bt_open = tk.Button(frame2, text ="Abrir", command = abrir)
bt_open.place(relx=0.25, rely=0.27, relwidth=0.5, relheight=0.1)

bt_ident = tk.Button(frame2, text ="Identificar", command = identify)
bt_ident.place(relx=0.25, rely=0.38, relwidth=0.5, relheight=0.1)

bt_train = tk.Button(frame2, text ="Atualizar Banco", command = update_facebank)
bt_train.place(relx=0.25, rely=0.49, relwidth=0.5, relheight=0.1)

boundingbox_flag = tk.IntVar()
c = tk.Checkbutton(frame4,text="Bounding Boxes", variable=boundingbox_flag)
c.pack()

window.mainloop()
