import subprocess
import sys
from pathlib import Path
import time
import signal

def start_ioc_subprocess() -> subprocess.Popen:
    here = Path(__file__).absolute().parent
    args = [sys.executable, "-m", "epicscorelibs.ioc", "-d", str(here/"record.db")]
    process = subprocess.Popen(
        args,
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        universal_newlines=True,
    )
    return process

process = start_ioc_subprocess()

def stop_process(signum, frame):
    print("****IOC output")
    print(process.communicate("exit")[0])
    sys.exit()

signal.signal(signal.SIGTERM, stop_process)
time.sleep(60)
