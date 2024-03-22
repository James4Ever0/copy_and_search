import multiprocessing
import keyboard
import clipboard
import ui

processes = {}


def run_keyboard_listener():
    keyboard.main()


def run_clipboard_listener():
    clipboard.main()


def start_process(runner, name: str):
    process = multiprocessing.Process(target=runner, daemon=True)
    processes[name] = process
    process.start()


if __name__ == "__main__":
    start_process(run_keyboard_listener, "keyboard_listener")
    start_process(run_clipboard_listener, "clipboard_listener")

    ui.ui_main()
