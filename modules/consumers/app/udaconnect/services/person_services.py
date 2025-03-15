import logging

from typing import Dict

from app.udaconnect.infra.database import DBSession
from app.udaconnect.models.person import Person
from app.udaconnect.models.schemas import PersonSchema

logging.basicConfig(level=logging.WARNING)
logger = logging.getLogger("udaconnect-consumer-person-svc")

session = DBSession()


class PersonService:
    @staticmethod
    def create(person: Dict):
        """
        Validate and persist a person model to DB.

        :param person: A Person dict
        """

        validation_results: Dict = PersonSchema().validate(person)
        if validation_results:
            logger.warning(
                f"Unexpected data format in payload: {validation_results}")
            raise Exception(f"Invalid payload: {validation_results}")

        new_person = Person()
        new_person.first_name = person["first_name"]
        new_person.last_name = person["last_name"]
        new_person.company_name = person["company_name"]

        session.add(new_person)
        session.commit()

        logger.info(f"New person persisted: {new_person.id}")
