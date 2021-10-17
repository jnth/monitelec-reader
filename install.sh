#!/usr/bin/env sh

# Installation of monitelec-reader

[ "$(id -u)" -eq 0 ] || { echo "You need to be ROOT (sudo can be used)"; exit 1; }

echo "Creating virtual environment"
rm -rf /opt/monitelec-reader
python3 -m venv /opt/monitelec-reader
source /opt/monitelec-reader/bin/activate

echo "Installing monitelec-reader"
python3 -m pip install -U pip wheel
python3 -m pip install -U monitelec-reader --trusted-host majordome --extra-index-url http://majordome:8050/api/v4/projects/5/packages/pypi/simple

echo "Setting service"
mkdir -p /opt/monitelec-reader/log
monitelec-reader-generate-service > /etc/systemd/system/monitelec-reader.service
chmod 644 /etc/systemd/system/monitelec-reader.service
systemctl enable monitelec-reader.service
