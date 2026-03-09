import psutil
import time

START_TIME = time.time()


def check_system():

    cpu = psutil.cpu_percent(interval=0.1)

    memory = psutil.virtual_memory()
    disk = psutil.disk_usage("/")

    uptime = time.time() - START_TIME

    return {
        "system": {
            "cpu_usage_percent": cpu,
            "memory_usage_percent": memory.percent,
            "disk_usage_percent": disk.percent,
            "uptime_seconds": int(uptime),
        }
    }
