from __future__ import annotations

import datetime
import re
import logging
import time

from monitelec_reader.config import settings
from monitelec_reader.record import Record
from monitelec_reader.tasks.mqtt import MqttTask

log = logging.getLogger("monitelec.flow")


# Pattern of one record from teleinfo flow
pattern = re.compile(
    r"\x0aADCO (?P<adco>\d+) .\x0d"
    r"\x0aOPTARIF (?P<optarif>.+) .\x0d"
    r"\x0aISOUSC (?P<isousc>\d+) .\x0d"
    r"\x0aHCHC (?P<hc>\d+) .\x0d"
    r"\x0aHCHP (?P<hp>\d+) .\x0d"
    r"\x0aPTEC (?P<ptec>.+) .\x0d"
    r"\x0aIINST (?P<iinst>\d+) .\x0d"
    r"\x0aIMAX (?P<imax>\d+) .\x0d"
    r"\x0aPAPP (?P<papp>\d+) .\x0d"
    r"\x0aHHPHC (?P<hhphc>.+) .\x0d"
    r"\x0aMOTDETAT (?P<motdetat>.+) .\x0d"
)


class Flow:
    """Serial data flow."""

    def __init__(self):
        self.message: str = ""
        self.mqtt_client = MqttTask(host=settings.mqtt.host, port=settings.mqtt.port, topic=settings.mqtt.topic,
                                    qos=settings.mqtt.qos)
        self.logger_level_interval = LoggerLevelInterval(max_duration=60)

    def reset(self):
        self.message = ""

    async def digest(self, raw: str):
        """Update message with new information."""
        self.message += raw

        # If a record is found, save it
        match = pattern.search(self.message)
        if match:
            record = Record(**match.groupdict(), dt_utc=datetime.datetime.utcnow())
            self.logger_level_interval(f"Record read: {record}")
            await self.mqtt_client.process_record(record)

            self.reset()  # reset flow


class LoggerLevelInterval:
    def __init__(self, max_duration=60):
        self.t = time.time()
        self.max_duration = max_duration

    def __call__(self, *args, **kwargs):
        now = time.time()
        if (now - self.t) > self.max_duration:
            self.t = now
            log.info(*args, **kwargs)
        else:
            log.debug(*args, **kwargs)
