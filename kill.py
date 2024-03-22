import requests
from config import HOST_ADDRESS, KILL_ENDPOINT, KILL_TIMEOUT
import fastapi
import uvicorn

def client_kill_server(port:int):
    kill_url = f"http://{HOST_ADDRESS}:{port}{KILL_ENDPOINT}"
    requests.get(kill_url, timeout=KILL_TIMEOUT)

def kill_and_run(app:fastapi.FastAPI,port:int):
    try:
        client_kill_server(port)
    except:
        pass
    uvicorn.run(app, host=HOST_ADDRESS, port=port)

def add_kill_endpoint(app:fastapi.FastAPI):
    def kill_server():
        exit()
    app.get(KILL_ENDPOINT)(kill_server)