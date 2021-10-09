"""Monitelec :: serial reader."""

from __future__ import annotations

import asyncio
import os
import sys
import time
import threading
import logging

import aioserial
import click

from monitelec_reader.flow import Flow
from monitelec_reader import generator
from monitelec_reader.log import configure_logs


log = logging.getLogger('monitelec.reader')


async def read_serial_teleinfo_data(device: str):
    """Read serial teleinfo data."""

    # Open serial device
    params = {
        'port': device,
        'baudrate': 1200,
        'bytesize': aioserial.SEVENBITS,
        'parity': aioserial.PARITY_EVEN,
        'stopbits': aioserial.STOPBITS_ONE,
    }

    serial = aioserial.AioSerial(**params)
    flow = Flow()
    log.info(f"Reading serial data on {device}")
    while True:
        raw = (await serial.read_async()).decode('utf-8')  # read serial data
        await flow.digest(raw)  # digest each received char


def wait_for(path: str, pause: int = 1, timeout: int = 5):
    """Wait for the existance of a path.

    :param path: path of check
    :param pause: pause between each tries (seconds)
    :param timeout: timeout (seconds)
    """
    time.sleep(0.25)
    t = time.time()
    while not os.path.exists(path):
        log.info(f"Waiting for {path}")
        time.sleep(pause)
        if time.time() - t > timeout:
            log.error(f"Cannot find {path}")
            sys.exit(1)


def launch_generator():
    """Launch the data generator (in a specific thread).

    :return: path of the device use by the generator
    """
    t = threading.Thread(target=generator.run)
    t.start()
    wait_for(path=generator.output_device)  # wait for the output device to be ready
    return generator.output_device


@click.command()
@click.option("-d", "--device", metavar="path", default="/tmp/serial", help="device to listen")
@click.option("--use-generator", is_flag=True, default=False, help="use data generator")
@click.option("-v", "--verbose", is_flag=True, default=False, help="verbose mode (debug)")
def main(device: str, use_generator: bool = False, verbose: bool = False):
    """monitelec-reader :: start the teleinfo data reader."""

    configure_logs(verbose)
    device = launch_generator() if use_generator else device

    # Check if the device exists
    if not os.path.exists(device):
        log.error(f"Device {device} does not exist")
        sys.exit(1)

    try:
        coro = read_serial_teleinfo_data(device=device)
        asyncio.run(coro)
    except KeyboardInterrupt:
        pass


if __name__ == '__main__':
    main()
