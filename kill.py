import requests
from config import HOST_ADDRESS, KILL_ENDPOINT, KILL_TIMEOUT, KILL_INTERVAL
import fastapi
import uvicorn
import time
import http
import os,signal
# from urllib3.exceptions import NewConnectionError
from requests.exceptions import ConnectionError
def client_kill_server(port:int):
    kill_url = f"http://{HOST_ADDRESS}:{port}{KILL_ENDPOINT}"
    try:
        response = requests.get(kill_url, timeout=KILL_TIMEOUT)
        return response.status_code
    except ConnectionError:
        return http.HTTPStatus.BAD_GATEWAY

def client_ensure_kill_server(port:int):
    while True:
        status_code = client_kill_server(port)
        if status_code == http.HTTPStatus.BAD_GATEWAY:
            break # 502, no such server.
        time.sleep(KILL_INTERVAL)

def kill_and_run(app:fastapi.FastAPI,port:int, application_name:str):
    print(f"[{application_name}] killing previous running server")
    client_ensure_kill_server(port)
    print(f"[{application_name}] starting server")
    add_kill_endpoint(app)
    uvicorn.run(app, host=HOST_ADDRESS, port=port)
    print(f"[{application_name}] shutting down server")


def add_kill_endpoint(app:fastapi.FastAPI):
    def kill_server():
        os.kill(os.getpid(), signal.SIGTERM)
    app.get(KILL_ENDPOINT)(kill_server)