"""Data generator."""

import os
import subprocess
import threading
import time
import logging

log = logging.getLogger("monitelec.generator")

root_dir = os.path.dirname(os.path.abspath(__file__))
path_dataflow = os.path.join(root_dir, "teleinfo.data")
input_device = "/tmp/input"
output_device = "/tmp/output"
char_sleep = 1 / 150.


def open_devices():
    log.info("Starting socat command to open devices")
    cmd = ["socat", "-d", "-d", f"pty,link={input_device},raw,echo=0", f"pty,link={output_device},raw,echo=0"]
    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    proc.communicate()


def read_data():
    """Read data store in disk."""

    with open(path_dataflow, 'rb') as f:
        raw = f.read()
    return raw


def run():
    log.debug("Reading local data...")
    raw = read_data()

    t = threading.Thread(target=open_devices)
    t.start()
    time.sleep(0.5)

    log.info(f"Starting flow on {output_device}...")
    try:
        with open(input_device, 'wb') as f:
            for char in raw:
                f.write(chr(char).encode('ascii'))
                f.flush()
                time.sleep(char_sleep)
    except KeyboardInterrupt:
        log.info("Cancelled by the user")
    except IOError:
        log.info("Stopped")
