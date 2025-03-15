import json
import logging

from kafka import KafkaProducer

logging.basicConfig(level=logging.WARNING)
logger = logging.getLogger("udaconnect-location-svc")


TOPIC_NAME = 'location'
KAFKA_SERVER = 'kafka:9092'

kafka_producer = KafkaProducer(bootstrap_servers=KAFKA_SERVER)


class LocationProducer:
    @staticmethod
    def send_message(location):
        """
        Produces message to Kafka location creation topic

        :param location: Location
        :param location: Location data to send
        :return:
        """
        kafka_producer.send(TOPIC_NAME, json.dumps(location).encode())
        kafka_producer.flush(timeout=5.0)
