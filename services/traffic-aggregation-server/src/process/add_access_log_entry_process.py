import json
from threading import Lock
from datetime import UTC
from datetime import datetime

from src.process.fetch_network_information_process import get_network_information

mutex = Lock()
access_log_data = []

def add_access_log_entry(log: str):
    with mutex:
        access_log = json.loads(log)
        network_info = get_network_information()
        network_name = access_log["request_X-Network-Name"]

        data = {
            "from": access_log["ClientHost"],
            "to": access_log["ServiceAddr"],
            "status": access_log["DownstreamStatus"],
            "ms": access_log["Duration"] / 1e6,
            "network": network_name,
            "timestamp": datetime.now(UTC).isoformat()
        }

        for i in network_info[network_name]["services"]:
            if i["ip"] == data["from"]:
                data["from"] = i["name"]

        access_log_data.append(data)

def get_access_logs():
    return access_log_data

def clear_access_logs(logs_to_remove: dict):
    with mutex:
        for item in logs_to_remove:
            if item in access_log_data:
                access_log_data.remove(item)
