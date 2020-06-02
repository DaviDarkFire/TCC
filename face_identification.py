#code based on https://www.pyimagesearch.com/2018/06/18/face-recognition-with-opencv-python-and-deep-learning/
import face_recognition
import os
import sys
import subprocess
import cv2
import pickle
import pathlib
import math
import time

facebank = ""
exit = ""
extensions = ['.jpg','.jpeg','.JPG','.JPEG','.PNG','.BMP']
flag = 1

def get_video_rotation(path):
    exit_file = "exit.txt"
    try:
        os.system(f'"exiftool.exe" -s -S -Rotation {os.path.relpath(path, os.getcwd())} > {exit_file}')
    except:
        print("Baixe o exiftool.exe e coloque-o na pasta build com o nome 'exiftool.exe'!!!")
        return
    f = open(exit_file,"r")
    rotation = int(f.read())
    f.close()
    os.remove("exit.txt")
    
    if (rotation == 270):
        rotation = cv2.ROTATE_90_COUNTERCLOCKWISE
    elif (rotation == 90):
        rotation = cv2.ROTATE_90_CLOCKWISE
    elif(rotation == 180):
        rotation = cv2.ROTATE_180
    elif(rotation == 0):
        rotation = -1

    return rotation

def generate_encodings_from_facebank(show_text, put_image): #adicionar verificação do banco de dados
    show_text("Atualizando banco de faces...\n Espere o término antes\n de fazer qualquer coisa.")
    knownEncodings = []
    knownNames = []
    for folder in os.listdir(facebank):
        show_text(f"{os.path.join(facebank,folder)}:")
        if(os.path.isdir(os.path.join(facebank,folder))):
            for image in os.listdir(os.path.join(facebank,folder)):
                if(os.path.splitext(image)[1] in extensions):
                    show_text(f"Adicionando: {image}", mode=0)
                    name = folder
                    imagePath = os.path.join(os.path.join(facebank,folder), image)
                    image = cv2.imread(imagePath)
                    rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
                    boxes = face_recognition.face_locations(rgb,model='CNN')
                    encodings = face_recognition.face_encodings(rgb, boxes)
                    for encoding in encodings:
                        knownEncodings.append(encoding)
                        knownNames.append(name)
    data = {"encodings": knownEncodings, "names": knownNames}
    try:
        f = open("face_encodings\encodings", "wb")
        f.write(pickle.dumps(data))
        f.close()
        show_text("texts/text3.txt")
        put_image(1)
    except:
        show_text("Não foi possível atualizar o Banco de Faces!!!")
    return

def save_img_with_bb(boxes, names, path):
    image = cv2.imread(path)
    for ((top, right, bottom, left), name) in zip(boxes, names):
        cv2.rectangle(image, (left, top), (right, bottom), (0, 255, 0), 2)
        y = top - 15 if top - 15 > 15 else top + 15
        cv2.putText(image, name, (left, y), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 255, 0), 2)

    nome =  os.path.basename(os.path.normpath(path))
    saida = os.path.join(exit, nome)
    cv2.imwrite(saida, image)

def get_formated_timestamp(milliseconds):
    tempo = milliseconds/1000
    if(tempo > 60):
        tempo = tempo/60.0
        if (tempo > 60):
            tempo = tempo/60.0
            minutos, horas = math.modf(tempo)
            minutos *= 60
            segundos, minutos = math.modf(minutos)
            return f"{int(horas):02d}:{int(minutos):02d}:{int(segundos*60):02d}"
        segundos, minutos = math.modf(tempo)
        segundos *= 60 
        return f"{int(minutos):02d}:{int(segundos):02d}"
    return f"{int(tempo):02d} segundos"

def recog_faces(path,bb_flag, show_text): #adicionar verificação pra ver se tem encodings
    try:
        show_text("Identificando imagens...")
        data = pickle.loads(open("face_encodings/encodings", "rb").read())
    except:
        show_text("Problema ao carregar Banco de Dados, experimente atualizar o banco corretamente!!!")
        return
    f = open(os.path.join(exit,"img_predictions.txt"),"w")
    teste = os.path.join(exit,"img_predictions.txt")
    buff = f"Saídas em {teste}\n"
    for subdir, dirs, images in os.walk(path):
        for img in  images:
            if(os.path.splitext(img)[1] in extensions):
                try:
                    image = cv2.imread(os.path.join(subdir,img))
                except:
                    show_text(f"Problema ao carregar a imagem {img} !!!")
                    break
                rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
                boxes = face_recognition.face_locations(rgb,model="CNN")
                encodings = face_recognition.face_encodings(rgb, boxes)
                names = ""
                list_names = []
                for encoding in encodings:
                    matches = face_recognition.compare_faces(data["encodings"],encoding)
                    name = "Desconhecido"
                    if True in matches:
                        matchedIdxs = [i for (i, b) in enumerate(matches) if b]
                        counts = {}
                        for i in matchedIdxs:
                            name = data["names"][i]
                            counts[name] = counts.get(name, 0) + 1
                        name = max(counts, key=counts.get)
                    names += f"{name} "
                    list_names.append(name)
                f.write(f"{img}: {names}\n")
                show_text(f"{img}: {names}",mode=0)
                buff += f"{img}: {names}\n"
                if(bb_flag):
                    save_img_with_bb(boxes,list_names,os.path.join(path,img))
    f.close()
    show_text(buff)
    if (flag):
        imageViewerFromCommandLine = {'linux':'xdg-open','win32':'explorer','darwin':'open'}[sys.platform]
        subprocess.run([imageViewerFromCommandLine, exit])
    return

def recog_faces_in_video(video_path, bb_flag, show_text): #adicionar verificação pra ver se tem encodings
    try:
        data = pickle.loads(open("face_encodings/encodings", "rb").read())
    except:
        show_text("Problema ao carregar Banco de Dados, experimente atualizar o banco corretamente!!!")
        return
    
    try:
        video = cv2.VideoCapture(video_path)
    except:
        show_text(f"Problema ao carregar video {video_path}!!!")
        return


    rotation = get_video_rotation(video_path)
    video_name =  os.path.splitext(os.path.basename(video_path))[0]
    f = open(os.path.join(exit,f"{video_name}.txt"),"w")
    print(os.path.join(exit,f"{video_name}"))

    show_text(f"Identificando no vídeo {video_name}", mode=0)

    if(bb_flag):
        fps = video.get(cv2.CAP_PROP_FPS)
        width = int(video.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))
        fourcc = cv2.VideoWriter_fourcc(*'MJPG')
        if(rotation == cv2.ROTATE_90_COUNTERCLOCKWISE or rotation == cv2.ROTATE_90_CLOCKWISE):
            output_video = cv2.VideoWriter(os.path.join(exit,f"{video_name}.mp4"), fourcc, fps, (height,width))
        else:
            output_video = cv2.VideoWriter(os.path.join(exit,f"{video_name}.mp4"), fourcc, fps, (width,height))

    j = 0
    while True:
        ret, frame = video.read()

        if(not ret):
            break

        if(rotation != -1):
            frame = cv2.rotate(frame,rotation)
    
        boxes = face_recognition.face_locations(frame,model="CNN")
        encodings = face_recognition.face_encodings(frame, boxes)
        names = ""
        list_names = []
        for encoding in encodings:
            matches = face_recognition.compare_faces(data["encodings"],encoding)
            name = "Desconhecido"
            if True in matches:
                matchedIdxs = [i for (i, b) in enumerate(matches) if b]
                counts = {}
                for i in matchedIdxs:
                    name = data["names"][i]
                    counts[name] = counts.get(name, 0) + 1
                name = max(counts, key=counts.get)
            f.write(f"{name} em {get_formated_timestamp(video.get(cv2.CAP_PROP_POS_MSEC))}\n")
            list_names.append(name)

        for ((top, right, bottom, left), name) in zip(boxes, list_names):
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
            y = top - 15 if top - 15 > 15 else top + 15
            cv2.putText(frame, name, (left, y), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 255, 0), 2)
        j += 1
        print(f"Escrevendo {j} frame, {video.get(cv2.CAP_PROP_POS_MSEC)} ms")
        if(bb_flag):
            output_video.write(frame)
    video.release()
    if(bb_flag):
        output_video.release()
    cv2.destroyAllWindows()
    f.close()
    show_text(os.path.join(exit,f"{video_name}.txt"), mode=0)
    imageViewerFromCommandLine = {'linux':'xdg-open','win32':'explorer','darwin':'open'}[sys.platform]
    subprocess.run([imageViewerFromCommandLine, exit])
    return
