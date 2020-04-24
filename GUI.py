import tkinter as tk
import face_identification as face_id
from tkinter import filedialog
import os
class GUI():
    def __init__(self):
        self.path = " "
        self.video_extensions = ['.mp4', '.m4a', '.m4v', '.f4v', '.f4a', '.m4b', '.m4r', '.f4b', '.mov','.wmv', '.wma', '.webm', '.flv','.avi','.mkv','.vob']
        ###################################################Criação base da janela
        self.window = tk.Tk()
        self.window.title("Face Identification")
        self.canvas = tk.Canvas(self.window, width=600, height=400) #o canvas serve pra dar um tamanho
        self.canvas.pack()
        self.frame_esq = tk.Frame(self.window)
        self.frame_esq.place(relx=0.05, rely=0.05,relwidth=0.45, relheight=0.9)
        self.frame_dir = tk.Frame(self.window)
        self.frame_dir.place(relx=0.5, rely=0.05,relwidth=0.45, relheight=0.9)
        self.frame_show = tk.Frame(self.frame_esq, highlightbackground="black", highlightthickness=1)
        self.frame_show.place(relx=0.1, rely=0.1,relwidth=0.8, relheight=0.8)
        self.frame_checkbox = tk.Frame(self.frame_dir)
        self.frame_checkbox.place(relx=-0.04, rely=0.66,relwidth=1, relheight=0.1)
        self.canvas_show = tk.Canvas(self.frame_show, width=600, height=600)
        self.canvas_show.pack()
        self.label = tk.Label(self.frame_esq,text='Mídia\Diretório', bd='3', fg='blue', font='Helvetica 9 bold')
        self.label.place(relx=0.0, rely=0.0, relwidth=0.5, relheight=0.05)
        ##################################################Criação de widgets
        self.bt_open = tk.Button(self.frame_dir, text ="Abrir", command = self.abrir)
        self.bt_open.place(relx=0.25, rely=0.27, relwidth=0.5, relheight=0.1)
        self.bt_ident = tk.Button(self.frame_dir, text ="Identificar", command = self.identify)
        self.bt_ident.place(relx=0.25, rely=0.38, relwidth=0.5, relheight=0.1)
        self.bt_train = tk.Button(self.frame_dir, text ="Atualizar Banco", command = self.update_facebank)
        self.bt_train.place(relx=0.25, rely=0.49, relwidth=0.5, relheight=0.1)
        self.boundingbox_flag = tk.IntVar()
        self.c = tk.Checkbutton(self.frame_checkbox,text="Bounding Boxes", variable=self.boundingbox_flag)
        self.c.pack()
        self.window.mainloop()

    def identify(self):
        if(self.path != " "):
            face_id.recog_faces(self.path,self.boundingbox_flag.get())
            for file in os.listdir(self.path):
                if(os.path.splitext(file)[1] in self.video_extensions):
                    face_id.recog_faces_in_video(f"{self.path}/{file}",self.boundingbox_flag.get())
            f = open("exit/img_predictions.txt","r") 
            buff = f.read()
            self.show_text(f"Video: video_predictions.txt\n{buff}")
        else:
            self.show_text("Selecione algum diretório.")

    def abrir(self):
        self.path 
        self.path = filedialog.askdirectory(parent=self.frame_esq,title='Escolha uma pasta com fotos e/ou vídeos')
        self.show_files(self.path)

    def show_text(self,buffer):
        self.canvas_show.delete("all")
        self.canvas_show.create_text(20, 20, anchor='nw' , text=buffer)

    def update_facebank(self):
        self.show_text("Atualizando encodings...")
        face_id.generate_encodings_from_facebank()
        self.show_text("Encodings salvos em: \n face_encodings\encodings")

    def show_files(self,path):
        self.canvas_show.delete("all")
        img_folder = path.split('/')[-1]
        strings = f"C:/.../{img_folder}\n"
        i = 20
        for file in os.listdir(path):
            strings += f"{file}\n"
            i += 20
        self.canvas_show.create_text(20, 20, anchor='nw' , text=strings) #n, ne, e, se, s, sw, self.canvas_show, nw
    
interface = GUI()