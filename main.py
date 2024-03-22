import multiprocessing
import ui
import sys, os, subprocess
from config import START_PROCESS_INTERVAL
import time

processes = {}


def run_python_script_as_subprocess(script_path: str):
    subprocess.run([sys.executable, script_path])


def resolve_script_relative_path(script_relative_path: str):
    basedir = os.path.split(__file__)[0]
    return os.path.join(basedir, script_relative_path)

def run_python_script_by_relative_path(script_relative_path:str):
    script_path = resolve_script_relative_path(script_relative_path)
    run_python_script_as_subprocess(script_path)

def run_keyboard_listener():
    # do not do that. it will not work.
    #     keyboard.main()
    run_python_script_by_relative_path("keyboard.py")

def run_clipboard_listener():
    run_python_script_by_relative_path("clipboard.py")

def start_process(runner, name: str):
    process = multiprocessing.Process(target=runner, daemon=True)
    processes[name] = process
    process.start()
    time.sleep(START_PROCESS_INTERVAL)

if __name__ == "__main__":
    start_process(run_keyboard_listener, "keyboard_listener")  # you cannot start it.
    start_process(run_clipboard_listener, "clipboard_listener")

    # keyboard.main()
    ui.ui_main()
