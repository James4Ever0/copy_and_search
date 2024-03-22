import multiprocessing
import ui
import sys, os, subprocess
from config import START_PROCESS_INTERVAL, CLIPBOARD_EVENT_PORT, KEYBOARD_EVENT_PORT
import time
from singleton import ensure_singleton
from kill import client_kill_server

processes = {}

def start_listeners():
    start_process(run_keyboard_listener, "keyboard_listener")
    start_process(run_clipboard_listener, "clipboard_listener")

def run_python_script_as_subprocess(script_path: str):
    subprocess.Popen([sys.executable, script_path])

def resolve_script_relative_path(script_relative_path: str):
    basedir = os.path.split(__file__)[0]
    return os.path.join(basedir, script_relative_path)

def run_python_script_by_relative_path(script_relative_path:str):
    script_path = resolve_script_relative_path(script_relative_path)
    run_python_script_as_subprocess(script_path)

def run_keyboard_listener():
    run_python_script_by_relative_path("keyboard.py")

def run_clipboard_listener():
    run_python_script_by_relative_path("clipboard.py")

def start_process(runner, name: str):
    process = multiprocessing.Process(target=runner, daemon=True)
    processes[name] = process
    process.start()
    time.sleep(START_PROCESS_INTERVAL)
    return process

def cleanup_processes():
    client_kill_server(CLIPBOARD_EVENT_PORT)
    client_kill_server(KEYBOARD_EVENT_PORT)

if __name__ == "__main__":
    ensure_singleton()
    start_listeners()

    ui.ui_main()
    
    cleanup_processes()