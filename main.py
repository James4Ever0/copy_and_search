import multiprocessing
import subprocess
import keyboard_event
import ui

def run_event_listener():
    keyboard_event.main()

if __name__ == '__main__':
    processes = {}
    
    event_listener_process = multiprocessing.Process(target=run_event_listener, daemon=True)
    processes['event_listener'] = event_listener_process
    event_listener_process.start()
    
    ui.ui_main()