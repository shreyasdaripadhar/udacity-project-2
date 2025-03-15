import json
import logging
from builtins import staticmethod

from kafka import KafkaProducer

logging.basicConfig(level=logging.WARNING)
logger = logging.getLogger("udaconnect-person-prd")


TOPIC_NAME = 'person'
KAFKA_SERVER = 'kafka:9092'

kafka_producer = KafkaProducer(bootstrap_servers=KAFKA_SERVER)


class PersonProducer:
    @staticmethod
    def send_message(person):
        kafka_producer.send(TOPIC_NAME, json.dumps(person).encode())
        kafka_producer.flush(timeout=5.0)
