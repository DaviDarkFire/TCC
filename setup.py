import sys
from cx_Freeze import setup, Executable

# Dependencies are automatically detected, but it might need fine tuning.
build_exe_options = {"packages": ["os","pkg_resources.py2_warn"], "include_files": ["face_encodings/","exiftool.exe","texts/","img/"]}

# GUI applications require a different base on Windows (the default is for a
# console application).
base = None
if sys.platform == "win32":
    base = "Win32GUI"

setup(  name = "Face Identification",
        version = "0.1",
        description = "Face Identification with GUI",
        options = {"build_exe": build_exe_options},
        executables = [Executable("FaceId.py", base=base, icon="img/icon2.png")])