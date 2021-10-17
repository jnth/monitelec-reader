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


## Build and publish

We use `poetry` to build package:

```shell
poetry-dynamic-versioning
poetry build
```

Publish in `majordome` GitLab:

```shell
poetry publish -r gitlab-majordome
```

__Note: use `POETRY_HTTP_BASIC_GITLAB_MAJORDOME_USERNAME` and `POETRY_HTTP_BASIC_GITLAB_MAJORDOME_PASSWORD`
to define GitLab credentials.__ It's normally in `~/.env`.


## Installation

Use:

```shell
curl http://majordome:8050/jonathan/monitelec-reader/-/raw/main/install.sh | sudo bash
```