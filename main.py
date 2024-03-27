# import multiprocessing
import threading
import ui
# import sys, subprocess
import os, signal
from config import START_PROCESS_INTERVAL, CLIPBOARD_EVENT_PORT, KEYBOARD_EVENT_PORT
import time
from singleton import ensure_singleton
from kill import client_kill_server
# let's instead improvise.
import clipboard, keyboard

# processes = {}

def start_listeners():
    start_thread(run_keyboard_listener)
    start_thread(run_clipboard_listener)
    # start_process(run_keyboard_listener, "keyboard_listener")
    # start_process(run_clipboard_listener, "clipboard_listener")

def start_thread(runner):
    thread = threading.Thread(target=runner, daemon=True).start()
    time.sleep(START_PROCESS_INTERVAL)
    return thread

# def run_python_script_as_subprocess(script_path: str):
#     subprocess.Popen([sys.executable, script_path]) # not applicable in this case.

# def resolve_script_relative_path(script_relative_path: str):
#     basedir = os.path.split(__file__)[0]
#     return os.path.join(basedir, script_relative_path)

# def run_python_script_by_relative_path(script_relative_path:str):
#     script_path = resolve_script_relative_path(script_relative_path)
#     run_python_script_as_subprocess(script_path)

def run_keyboard_listener():
    # run_python_script_by_relative_path("keyboard.py")
    keyboard.main()
    # runpy.run_module("mouse", run_name="__main__")

def run_clipboard_listener():
    # run_python_script_by_relative_path("clipboard.py")
    clipboard.main()

# def start_process(runner, name: str):
#     process = multiprocessing.Process(target=runner, daemon=True)
#     processes[name] = process
#     process.start()
#     time.sleep(START_PROCESS_INTERVAL)
#     return process

def cleanup():
    client_kill_server(CLIPBOARD_EVENT_PORT)
    client_kill_server(KEYBOARD_EVENT_PORT)

def main():
    start_listeners()
    with ensure_singleton():
        print("[main] ui started.")
        ui.ui_main()
        # start_process(ui.ui_main, 'ui_process').join()
        # start_thread(ui.ui_main).join()
        
        print("[main] cleaning up.")
        cleanup()
        print("[main] exiting.")
    os.kill(os.getpid(), signal.SIGTERM)

if __name__ == "__main__":
    main()