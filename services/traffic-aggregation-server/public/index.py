import asyncio
import json

from fastapi import FastAPI, WebSocket
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
import docker

from src.process.add_access_log_entry_process import get_access_logs, clear_access_logs
from src.process.fetch_network_information_process import get_network_information
from src.process.watch_logfile_process import watch_logfile

docker_client = docker.DockerClient(base_url="unix://var/run/docker.sock")
app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

watch_logfile("/var/log/access-log.log")

@app.get("/", response_class=HTMLResponse)
def get_index():
    with open("static/index.html") as f:
        return f.read()

@app.websocket("/access_logs")
async def access_logs_websocket(websocket: WebSocket):
  await websocket.accept()
  while True:
    data = get_access_logs()
    await websocket.send_text(json.dumps(data))
    if len(data) > 0:
        print(data, flush=True)
    clear_access_logs(data)
    await asyncio.sleep(0.01)

@app.get("/network_info")
async def ping():
  return get_network_information()

