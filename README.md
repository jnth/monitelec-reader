# monitelec-reader

Read and process the serial teleinfo data.

Dedicated to be run by a Raspberry Pi Zero connected to the electric meter.


## Usage

Configure the application in `settings.toml` and `.secrets.toml` file (use the last one for sensitive data like
passwords). In production, configuration can be set in `~/.monitelec-reader.toml`.


### Read and process the data flow

Run the command `teleinfo-serial-reader` to read the data flow and send useful information with MQTT.

Use `teleinfo-serial-reader --help` to show command usage.


## How to simulate teleinfo serial data

Use the `--use-generator` option of the `teleinfo-serial-reader` script.

