from PIL import Image
import os
import cv2

def generate_id(name):
    id = "_"
    for i in range(3):
        id = id+str(ord(os.urandom(1)))
    return f"{id}_{name}"

def update_facebank_with_unique_id():
    for folder_name in os.listdir(FACEBANK):
        if folder_name[0] != '_':
            os.rename(f"{FACEBANK}/{folder_name}",f"{FACEBANK}/{generate_id(folder_name)}")

def get_video_rotation(path):
    exit_file = "exit.txt"
    os.system(f'"exiftool.exe" -s -S -Rotation {path} > {exit_file}')
    f = open(exit_file,"r")
    rotation = int(f.read())
    f.close()
    os.remove("exit.txt")
    
    if (rotation == 270):
        print("VIADOW1")
        rotation = cv2.ROTATE_90_COUNTERCLOCKWISE
    elif (rotation == 90):
        print("VIADOW2")
        rotation = cv2.ROTATE_90_CLOCKWISE
    elif(rotation == 180):
        print("VIADOW3")
        rotation = cv2.ROTATE_180
    elif(rotation == 0):
        print("VIADOW4")
        rotation = -1

    return rotation
