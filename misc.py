from PIL import Image
import qtrotate as cu

def generate_id(name):
    id = "_"
    for i in range(3):
        id = id+str(ord(os.urandom(1)))
    return f"{id}_{name}"

def update_facebank_with_unique_id():
    for folder_name in os.listdir(FACEBANK):
        if folder_name[0] != '_':
            os.rename(f"{FACEBANK}/{folder_name}",f"{FACEBANK}/{generate_id(folder_name)}")

print(cu.get_set_rotation("video2.mp4"))
