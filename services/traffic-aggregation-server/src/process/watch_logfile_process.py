import threading
import time

import docker

from src.process.add_access_log_entry_process import add_access_log_entry

def watch_logfile(logfile: str, network_name: str):
    def watch_file_subprocess():
        docker_client = docker.from_env()
        with open(logfile) as f:
            f.seek(0, 2)
            while True:
                log = f.readline()
                if log:
                    add_access_log_entry(docker_client, network_name, log)
                else:
                    time.sleep(1)

    threading.Thread(target=watch_file_subprocess, daemon=True).start()
