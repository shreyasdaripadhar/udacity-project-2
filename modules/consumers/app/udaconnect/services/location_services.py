import logging

from geoalchemy2.functions import ST_Point
from typing import Dict

from app.udaconnect.infra.database import DBSession
from app.udaconnect.models.location import Location
from app.udaconnect.models.schemas import LocationSchema

logging.basicConfig(level=logging.WARNING)
logger = logging.getLogger("udaconnect-consumer-location-svc")

session = DBSession()


class LocationService:
    @staticmethod
    def create(location: Dict):
        """
        Validate and persists a location model to DB.

        :param location: A Location dict
        """

        validation_results: Dict = LocationSchema().validate(location)
        if validation_results:
            logger.warning(
                f"Unexpected data format in payload: {validation_results}")
            raise Exception(f"Invalid payload: {validation_results}")

        new_location = Location()
        new_location.person_id = location["person_id"]
        new_location.coordinate = ST_Point(
            location["latitude"], location["longitude"])
        session.add(new_location)
        session.commit()

        logger.info(f"New location persisted: {new_location.id}")
