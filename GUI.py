import tkinter as tk
import face_identification as face_id
from tkinter import filedialog
import os
import threading
import ctypes
import time

class GUI():
    def __init__(self):
        self.show_text_height = 0
        self.path = " "
        self.video_extensions = ['.mp4', '.m4a', '.m4v', '.f4v', '.f4a', '.m4b', '.m4r', '.f4b', '.mov','.wmv', '.wma', '.webm', '.flv','.avi','.mkv','.vob']
        ###################################################Criação base da janela
        self.window = tk.Tk()
        self.window.title("Face Identification")
        user32 = ctypes.windll.user32
        self.canvas = tk.Canvas(self.window, width=user32.GetSystemMetrics(0), height=user32.GetSystemMetrics(1)) #o canvas serve pra dar um tamanho
        self.canvas.pack()
        self.frame_esq = tk.Frame(self.window)
        self.frame_esq.place(relx=0.05, rely=0.05,relwidth=0.45, relheight=0.9)
        self.frame_dir = tk.Frame(self.window)
        self.frame_dir.place(relx=0.5, rely=0.05,relwidth=0.45, relheight=0.9)
        self.frame_show = tk.Frame(self.frame_esq, highlightbackground="black", highlightthickness=1)
        self.frame_show.place(relx=0.1, rely=0.1,relwidth=0.8, relheight=0.8)
        self.frame_checkbox = tk.Frame(self.frame_dir)
        self.frame_checkbox.place(relx=0.00, rely=0.66,relwidth=1, relheight=0.1)
        self.canvas_show = tk.Canvas(self.frame_show, width=600, height=600, bg="white")
        self.canvas_show.pack()
        self.label = tk.Label(self.frame_esq,text='Mídia\Diretório', bd='3', fg='blue', font='Helvetica 9 bold')
        self.label.place(relx=0.0, rely=0.0, relwidth=0.5, relheight=0.05)
        ##################################################Criação de widgets
        self.bt_train = tk.Button(self.frame_dir, text ="1º Atualizar Banco de Faces", command = self.update_facebank)
        self.bt_train.place(relx=0.25, rely=0.38, relwidth=0.5, relheight=0.1)
        # self.bt_open = tk.Button(self.frame_dir, text ="2º Abrir Pasta com Faces Desconhecidas", command = self.abrir)
        # self.bt_open.place(relx=0.25, rely=0.44, relwidth=0.5, relheight=0.1)
        self.bt_ident = tk.Button(self.frame_dir, text ="2º Identificar Faces Desconhecidas", command = self.identify)
        self.bt_ident.place(relx=0.25, rely=0.50, relwidth=0.5, relheight=0.1)
        self.boundingbox_flag = tk.IntVar()
        self.c = tk.Checkbutton(self.frame_checkbox,text="Bounding Boxes", variable=self.boundingbox_flag)
        self.c.select()
        self.c.pack()
        #self.show_text("texts/text1.txt", mode=1)
        self.imgs = []
        self.imgs.append(tk.PhotoImage(file="img/teste.png"))
        self.imgs.append(tk.PhotoImage(file="img/teste2.png"))
        self.put_image(0)
        self.create_folders()
        self.window.mainloop()

    def put_image(self, i):
        if(i == 0):
            self.canvas_show.create_image(20, 10, image=self.imgs[i], anchor='nw')
        elif(i == 1):
            self.canvas_show.create_image(20, self.show_text_height, image=self.imgs[i], anchor='nw')
        # elif(i == 2):
        #     self.canvas_show.create_image(20,self.show_text_height, image=self.imgs[i], anchor='nw')
        # elif(i == 3):
        #     self.canvas_show.create_image(80, self.show_text_height, image=self.imgs[i], anchor='nw')

    def identify_video(self):
        for file in os.listdir(self.path):
            if(os.path.splitext(file)[1] in self.video_extensions):
                face_id.recog_faces_in_video(f"{self.path}/{file}",self.boundingbox_flag.get(),self.show_text)
        return

    def identify(self):
        if(os.path.isdir(self.path)):
            t_img = threading.Thread(target=face_id.recog_faces, args=(self.path, self.boundingbox_flag.get(),self.show_text,))
            t_img.start()
            t_video = threading.Thread(target=self.identify_video)
            t_video.start()
        else:
            self.show_text("Selecione algum diretório.")
    
    def create_folders(self):
        desktop = os.path.normpath(os.path.join(os.environ['USERPROFILE'], 'Desktop'))
        face_id.facebank = os.path.normpath(os.path.join(desktop,'banco_de_faces'))
        face_id.exit = os.path.normpath(os.path.join(desktop,'saida'))
        self.path = os.path.normpath(os.path.join(desktop,'faces_desconhecidas'))

        if(not os.path.exists(face_id.facebank)):
            try:
                os.mkdir(face_id.facebank)
            except OSError:
                print ("Problema ao criar pasta 'banco_de_faces/'")

        if(not os.path.exists(self.path)):
            try:
                os.mkdir(self.path)
            except OSError:
                print ("Problema ao criar pasta 'faces_desconhecidas/'") 

        if(not os.path.exists(face_id.exit)):
            try:
                os.mkdir(face_id.exit)
            except OSError:
                print ("Problema ao criar pasta 'saida/'") 


    # def abrir(self):
    #     self.path = filedialog.askdirectory(parent=self.frame_esq,title='Escolha uma PASTA com fotos e/ou vídeos')
    #     print(self.path)
    #     if(os.path.isdir(self.path)):
    #         self.show_files(self.path)
    #         self.show_text("texts/text4.txt",mode=0)
    #         self.put_image(3)

    # def abrir_banco_faces(self):
    #     face_id.facebank = filedialog.askdirectory(parent=self.frame_esq,title='Escolha o diretório com faces criado por você:')
    #     print(face_id.facebank)
    #     if(os.path.isdir(face_id.facebank)):
    #         self.show_files(face_id.facebank)
    #         self.show_text("texts/text2.txt",mode=0)
    #         self.put_image(1)

    def show_text(self,buffer, mode=1): #mode 1 => delete all text and write a new one, mode 0 => apend text
        if(os.path.isfile(buffer)):
            f = open(buffer,"r") 
            buffer = f.read()
        if(mode):
            self.canvas_show.delete("all")
            myText = self.canvas_show.create_text(20, 20, anchor='nw' , text=buffer)
            bounds = self.canvas_show.bbox(myText)
            self.show_text_height = bounds[3] - bounds[1] + 9 #CATAPIMBAS CONFRADE IS THAT A GAMBITO REFERENCE?
        else:
            myText = self.canvas_show.create_text(20, self.show_text_height+10, anchor='nw' , text=buffer)
            bounds = self.canvas_show.bbox(myText)
            self.show_text_height += bounds[3] - bounds[1] + 9
        return

    def update_facebank(self):
        t = threading.Thread(target=face_id.generate_encodings_from_facebank, args=(self.show_text,self.put_image))
        t.start()
        # face_id.generate_encodings_from_facebank()
        # self.show_text("Encodings salvos em: \n face_encodings\encodings")

    def show_files(self,path):
        self.canvas_show.delete("all")
        img_folder = path.split('/')[-1]
        strings = f"C:/.../{img_folder}\n"
        i = 20
        for file in os.listdir(path):
            if(os.path.isdir(f"{path}/{file}")):
                strings += f"          {file}/\n"
            else:
                strings += f"          {file}\n"
            i += 20
        myText = self.canvas_show.create_text(20, 20, anchor='nw' , text=strings) #n, ne, e, se, s, sw, self.canvas_show, nw
        bounds = self.canvas_show.bbox(myText)
        self.show_text_height = bounds[3] - bounds[1] + 9
    
if __name__ == '__main__':
    interface = GUI()