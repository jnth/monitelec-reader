"""Generate systemctl service."""

import os

rootdir = os.path.dirname(os.path.abspath(__file__))
service_path = os.path.join(rootdir, 'share', 'monitelec-reader.service')


def generate_service():
    with open(service_path) as f:
        for line in f.readlines():
            print(line.rstrip())
