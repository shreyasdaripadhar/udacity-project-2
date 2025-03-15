import json
import logging
import threading

from app.udaconnect.services.person_services import PersonService
from kafka import KafkaConsumer

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("person-consumer")

TOPIC_NAME = 'person'


class PersonConsumer(threading.Thread):
    """
    Non blocking kafka consumer.
    Base on kafka-python examples @
    https://github.com/dpkp/kafka-python/blob/master/example.py
    """
    def __init__(self, kafka_server):
        threading.Thread.__init__(self)
        self.stop_event = threading.Event()
        self.kafka_server = kafka_server

    def stop(self):
        self.stop_event.set()

    def run(self):
        logger.info('Starting Person Topic Consumer')

        consumer = KafkaConsumer(bootstrap_servers=self.kafka_server,
                                 consumer_timeout_ms=1000,
                                 group_id='person-group')
        consumer.subscribe(TOPIC_NAME)

        while not self.stop_event.is_set():
            for message in consumer:
                PersonService.create(json.loads(message.value.decode('utf-8')))
                if self.stop_event.is_set():
                    break

        logger.info('Stopping Person Topic Consumer')
        consumer.close()
