import logging
from builtins import staticmethod
from typing import Dict, List

from app import db
from app.udaconnect.models.person import Person
from app.udaconnect.producers.person_producer import PersonProducer

logging.basicConfig(level=logging.WARNING)
logger = logging.getLogger("udaconnect-person-svc")


class PersonService:

    @staticmethod
    def create(person: Dict):
        PersonProducer.send_message(person)

    @staticmethod
    def retrieve(person_id: int) -> Person:
        person = db.session.query(Person).get(person_id)
        return person

    @staticmethod
    def retrieve_all() -> List[Person]:
        return db.session.query(Person).all()
