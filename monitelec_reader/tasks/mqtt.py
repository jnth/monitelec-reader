import logging
import pathlib
import random
import string

from paho.mqtt.client import Client
from monitelec_reader.flow import Record

log = logging.getLogger('monitelec.tasks.mqtt')

characters = string.ascii_letters * 2 + string.digits


def random_id():
    return "".join(random.sample(characters, k=6))


class Topic(pathlib.PosixPath):
    pass


class MqttTask:
    def __init__(self, host, port, topic, qos=0):
        self.host = host
        self.port = port
        self.topic = Topic(topic)
        self.qos = qos
        self.mqtt_client = Client(client_id=f"monitelec-reader-{random_id()}")
        self.mqtt_client.connect(host=self.host, port=self.port, keepalive=10)
        log.info(f"Connected to MQTT {self.host}:{self.port}")

    def __del__(self):
        self.mqtt_client.disconnect()

    def __publish(self, topic: Topic, payload: str):
        self.mqtt_client.publish(topic=str(topic), payload=payload, qos=self.qos)
        self.mqtt_client.loop()

    async def process_record(self, record: Record):
        topic = self.topic / 'record'
        payload = record.as_json()
        self.__publish(topic, payload)
        log.debug(f"Record send in topic {topic}: {payload}")
