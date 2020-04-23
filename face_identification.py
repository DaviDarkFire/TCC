#code based on https://www.pyimagesearch.com/2018/06/18/face-recognition-with-opencv-python-and-deep-learning/
import face_recognition
import misc
import os
import cv2
import pickle
import pathlib

FACEBANK = "facebank"
extensions = ['.jpg','.jpeg','.JPG','.JPEG','.PNG','.BMP']

def generate_encodings_from_facebank():
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

def recog_faces(path,bb_flag):
    data = pickle.loads(open("face_encodings/encodings", "rb").read())
    f = open("predictions.txt","w")
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
                if(bb_flag):
                    save_img_with_bb(boxes,list_names,f"{subdir}/{img}")
    f.close()

def recog_faces_in_video(video_path, bb_flag):
    data = pickle.loads(open("face_encodings/encodings", "rb").read())
    video = cv2.VideoCapture(video_path)
    #rotation = misc.check_rotation(video_path)

    fps = video.get(cv2.CAP_PROP_FPS)
    width = int(video.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))

    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    output_video = cv2.VideoWriter('output.mp4', fourcc, fps, (width, height))
    j = 0
    while True:
        ret, frame = video.read()
        if(not ret):
            break
        #frame = misc.correct_rotation(frame,rotation)
        j += 1
        cv2.imwrite(f"exit/{j}_exit.jpg", frame)

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
            names += f"{name} "
            list_names.append(name)
            
        for ((top, right, bottom, left), name) in zip(boxes, list_names):
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
            y = top - 15 if top - 15 > 15 else top + 15
            cv2.putText(frame, name, (left, y), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 255, 0), 2)

        output_video.write(frame)
    video.release()
    output_video.release()

#generate_encodings_from_facebank()
recog_faces_in_video("video1.mp4",1)