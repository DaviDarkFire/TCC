from PIL import Image
import os

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
    return rotation

print(get_video_rotation("video____.mp4"))