import json
from threading import Lock

from docker import DockerClient

from src.process.fetch_network_information_process import fetch_network_information

mutex = Lock()
access_log_data = []

def add_access_log_entry(docker_client: DockerClient, network_name: str, log: str):
    with mutex:
        access_log = json.loads(log)
        network_info = fetch_network_information(docker_client)

        data = {
            "from": access_log["ClientHost"],
            "to": access_log["ServiceAddr"],
            "status": access_log["DownstreamStatus"],
            "ms": access_log["Duration"] / 1e6,
            "network": network_name,
        }

        for i in network_info[network_name]["services"]:
            print(i["ip"], data["from"], i["ip"] == data["from"])
            if i["ip"] == data["from"]:
                data["from"] = i["name"]


        access_log_data.append(data)
        print(access_log_data, flush=True)

def get_access_logs():
    return access_log_data