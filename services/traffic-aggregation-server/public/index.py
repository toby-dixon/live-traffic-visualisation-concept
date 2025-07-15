from fastapi import FastAPI
import docker

from src.process.add_access_log_entry_process import get_access_logs
from src.process.fetch_network_information_process import fetch_network_information
from src.process.watch_logfile_process import watch_logfile

docker_client = docker.DockerClient(base_url="unix://var/run/docker.sock")
app = FastAPI()

watch_logfile("/var/log/private-server-proxy.log", "private-server-proxy-network")

@app.get("/access_logs")
def ping():
  return get_access_logs()

@app.get("/network_info")
def ping():
  return fetch_network_information(docker_client)
