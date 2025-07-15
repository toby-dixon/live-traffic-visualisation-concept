import threading
import time

from src.process.add_access_log_entry_process import add_access_log_entry

def watch_logfile(logfile: str):
    def watch_file_subprocess():
        with open(logfile) as f:
            f.seek(0, 2)
            while True:
                log = f.readline()
                if log:
                    add_access_log_entry(log)
                else:
                    time.sleep(1)

    threading.Thread(target=watch_file_subprocess, daemon=True).start()
