import os

path = "C:\\Users\\davec\\Desktop\\banco_de_faces"
for pinto in os.listdir(path):
    if(os.path.isdir(os.path.join(path,pinto))):
        for file in os.listdir(os.path.join(path,pinto)):
            