from app.udaconnect.consumers.person_consumer import PersonConsumer
from app.udaconnect.consumers.location_consumer import LocationConsumer

KAFKA_SERVER = 'kafka:9092'


if __name__ == "__main__":
    PersonConsumer(kafka_server=KAFKA_SERVER).start()
    LocationConsumer(kafka_server=KAFKA_SERVER).start()
