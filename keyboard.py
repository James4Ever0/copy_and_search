import time
import threading
from fastapi import FastAPI
from config import KEYBOARD_EVENT_PORT, KEYBOARD_EVENT_ENDPOINT, HOST_ADDRESS
from dataclass import KeyboardEventTimestamp
# Listen to keyboard events
from pynput import keyboard
from kill import kill_and_run

latest_keypress_timestamp = 0

def update_latest_keypress_event_timestamp():
    global latest_keypress_timestamp
    latest_keypress_timestamp = time.time()
    print("[keyboard listener] updated timestamp:", latest_keypress_timestamp)

def on_press(key):
    update_latest_keypress_event_timestamp()

def on_release(key):
    update_latest_keypress_event_timestamp()

# Create a keyboard listener in a separate daemon thread
def keyboard_listener():
    with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()


# Create a FastAPI instance
app = FastAPI()

# Endpoint to get the latest key event timestamp
# @app.get("/latest_keypress_timestamp")
@app.get(KEYBOARD_EVENT_ENDPOINT)
async def get_keyboard():
    return KeyboardEventTimestamp(timestamp=latest_keypress_timestamp)

def main():
    
    # Create a keyboard listener in a separate daemon thread
    
    keyboard_thread = threading.Thread(target=keyboard_listener, daemon=True)
    keyboard_thread.start()

    # uvicorn.run(app, host="127.0.0.1", port=8991)
    print("[keyboard listener] starting server")
    kill_and_run(app, port=KEYBOARD_EVENT_PORT)

if __name__ == "__main__":
    main()