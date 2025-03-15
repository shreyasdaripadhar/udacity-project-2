from functools import lru_cache
from typing import List

from app.udaconnect.models import Location
from app.udaconnect.infra.database import DBSession

session = DBSession()


class LocationService:

    @staticmethod
    @lru_cache(maxsize=10)
    def fetch_locations(person_id, start_date, end_date) -> List:
        """
        Fetch locations for a person_id given a range of time.

        :param person_id: The person id to look for
        :param start_date: Start date (inclusive)
        :param end_date: End date (exclusive)
        :return: List
        """

        locations: List = session.query(Location).filter(
            Location.person_id == person_id
        ).filter(Location.creation_time < end_date).filter(
            Location.creation_time >= start_date
        ).all()

        return locations
