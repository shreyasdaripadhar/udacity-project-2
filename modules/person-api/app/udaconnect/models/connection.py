from __future__ import annotations

from dataclasses import dataclass

from app import db  # noqa

from app.udaconnect.models.location import Location
from app.udaconnect.models.person import Person


@dataclass
class Connection:
    location: Location
    person: Person
