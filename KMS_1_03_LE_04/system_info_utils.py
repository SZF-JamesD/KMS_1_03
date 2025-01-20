import platform
import os
from datetime import datetime

def collect_system_info():
    system_info = {
        "analysis_time": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        "os_name": platform.system(),
        "os_version": platform.version(),
        "os_release": platform.release(),
        "architecture": platform.architecture()[0],
        "python_version": platform.python_version(),
        "machine": platform.machine(),
        "processor": platform.processor(),
        "node": platform.node(),
        "python_path": os.path.abspath(os.__file__)
    }
    return system_info


if __name__ == "__main__":
    info = collect_system_info()
    for key, value in info.items():
        print(f"{key}: {value}")