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

FACEBANK = "facebank"
extensions = ['.jpg','.jpeg','.JPG','.JPEG','.PNG','.BMP']

def get_video_rotation(path):
    exit_file = "exit.txt"
    os.system(f'"exiftool.exe" -s -S -Rotation {os.path.relpath(path, os.getcwd())} > {exit_file}')
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

def generate_encodings_from_facebank(show_text): #adicionar verificação do banco de dados
    show_text("Atualizando banco de faces...\n Espere o término antes\n de fazer qualquer coisa.")
    knownEncodings = []
    knownNames = []
    for subdir, dirs, images in os.walk(FACEBANK):
        for image in  images:
            print(f"Encoding: {image}")
            print(subdir)
            name = subdir.split('\\')[1]
            imagePath = f"{subdir}\{image}"
            image = cv2.imread(imagePath)
            rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            boxes = face_recognition.face_locations(rgb,model='CNN')
            encodings = face_recognition.face_encodings(rgb, boxes)
            for encoding in encodings:
                knownEncodings.append(encoding)
                knownNames.append(name)
    data = {"encodings": knownEncodings, "names": knownNames}
    f = open("face_encodings\encodings", "wb")
    f.write(pickle.dumps(data))
    f.close()
    show_text("Banco de faces atualizado \n com sucesso!!!")
    return

def save_img_with_bb(boxes, names, path):
    image = cv2.imread(path)
    for ((top, right, bottom, left), name) in zip(boxes, names):
        cv2.rectangle(image, (left, top), (right, bottom), (0, 255, 0), 2)
        y = top - 15 if top - 15 > 15 else top + 15
        cv2.putText(image, name, (left, y), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 255, 0), 2)

    nome = os.path.splitext(path)[0].split('/')[-1] 
    ext = os.path.splitext(path)[1]
    caminho = pathlib.Path().absolute()
    cv2.imwrite(f"{caminho}/exit/{nome}_exit{ext}", image)

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
    show_text("Identificando imagens...")
    data = pickle.loads(open("face_encodings/encodings", "rb").read())
    f = open("exit/img_predictions.txt","w")
    buff = "Saídas em exit/img_predictions.txt \n"
    for subdir, dirs, images in os.walk(path):
        for img in  images:
            if(os.path.splitext(img)[1] in extensions):
                image = cv2.imread(f"{subdir}/{img}")
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
                buff += f"{img}: {names}\n"
                if(bb_flag):
                    save_img_with_bb(boxes,list_names,f"{subdir}/{img}")
    f.close()
    show_text(buff)
    imageViewerFromCommandLine = {'linux':'xdg-open','win32':'explorer','darwin':'open'}[sys.platform]
    subprocess.run([imageViewerFromCommandLine, f"{pathlib.Path().absolute()}\exit\\"])
    return

def recog_faces_in_video(video_path, bb_flag, show_text): #adicionar verificação pra ver se tem encodings
    data = pickle.loads(open("face_encodings/encodings", "rb").read())
    video = cv2.VideoCapture(video_path)
    rotation = get_video_rotation(video_path)
    video_name = video_path.split('/')[-1]
    f = open(f"exit/predictions_{video_name}.txt","w")

    if(bb_flag):
        fps = video.get(cv2.CAP_PROP_FPS)
        width = int(video.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))
        fourcc = cv2.VideoWriter_fourcc(*'MJPG')
        if(rotation == cv2.ROTATE_90_COUNTERCLOCKWISE or rotation == cv2.ROTATE_90_CLOCKWISE):
            output_video = cv2.VideoWriter(f"exit/predictions_{video_name}", fourcc, fps, (height,width))
        else:
            output_video = cv2.VideoWriter(f"exit/predictions_{video_name}", fourcc, fps, (width,height))

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
    show_text(f"exit/predictions_{video_name}\n", mode=0)
    return
