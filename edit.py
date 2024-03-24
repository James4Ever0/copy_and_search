import os, sys
import subprocess
import shutil

def open_file_in_editor(file_path):
    if os.name == "nt":  # Windows
        # os.system("start notepad.exe {}".format(file_path))
        # Specify the executable you want to locate
        executable_path = shutil.which("notepad.exe")
        subprocess.call([executable_path, file_path])
    elif os.name == "posix":  # macOS or Linux
        opener:list[str] = ["open", "-a", "TextEdit"] if sys.platform == "darwin" else ["xdg-open"]
        subprocess.call([*opener, file_path])
    else:
        print("Unsupported OS")
