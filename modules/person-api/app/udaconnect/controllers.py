from datetime import datetime
from typing import List, Optional

from flask import request
from flask_accepts import accepts, responds
from flask_restx import Namespace, Resource, fields

from app.udaconnect.models.connection import Connection
from app.udaconnect.models.location import Location
from app.udaconnect.models.person import Person
from app.udaconnect.schemas import ConnectionSchema, PersonSchema
from app.udaconnect.services.connection_service import ConnectionDataService
from app.udaconnect.services.person_service import PersonService

DATE_FORMAT = "%Y-%m-%d"

api = Namespace("UdaConnect", description="Provides person data")  # noqa

person_model = api.model('Person', {
    'id': fields.Integer,
    'first_name': fields.String,
    'last_name': fields.String,
    'company_name': fields.String
})

location_model = api.model('Location', {
        'id': fields.Integer,
        'person_id': fields.Integer,
        'longitude': fields.String,
        'latitude': fields.String,
        'creation_time': fields.DateTime
    })

connection_model = api.model('Connection', {
    'location': fields.Nested(location_model),
    'person': fields.Nested(person_model)
})


@api.route("/persons")
class PersonsResource(Resource):
    @accepts(schema=PersonSchema)
    @api.doc(description='Issues the creation of a new Location',
             body=person_model,
             responses={
                 202: 'Person creation accepted',
                 500: 'Internal server error'
             }
             )
    def post(self):
        payload = request.get_json()
        PersonService.create(payload)

        return {'status': 'accepted'}, 202

    @responds(schema=PersonSchema, many=True)
    @api.doc(description='List existing people',)
    @api.response(200, 'Listing successful', fields.List(fields.Nested(person_model)))
    def get(self) -> List[Person]:
        persons: List[Person] = PersonService.retrieve_all()
        return persons


@api.route("/persons/<person_id>")
@api.param("person_id", "Unique ID for a given Person", _in="query")
class PersonResource(Resource):
    @responds(schema=PersonSchema)
    @api.doc(description='Search for a given Person by its id',
             params={'person_id': 'Required person id'},
             responses={
                 404: 'Person not found',
                 500: 'Internal server error'
             },
             )
    @api.response(200, 'Person found', person_model)
    def get(self, person_id) -> Person:
        person: Person = PersonService.retrieve(person_id)
        return person


@api.route("/persons/<person_id>/connection")
@api.param("start_date", "Lower bound of date range", _in="query")
@api.param("end_date", "Upper bound of date range", _in="query")
@api.param("distance", "Proximity to a given user in meters", _in="query")
@api.doc(description='Search for connection data for a given person_id',
         model=connection_model)
class ConnectionDataResource(Resource):
    @responds(schema=ConnectionSchema, many=True)
    @api.response(200, 'Connection(s) found', fields.List(fields.Nested(connection_model)))
    def get(self, person_id) -> List[ConnectionSchema]:
        start_date: datetime = datetime.strptime(
            request.args["start_date"], DATE_FORMAT
        )
        end_date: datetime = datetime.strptime(
            request.args["end_date"], DATE_FORMAT)
        distance: Optional[int] = request.args.get("distance", 5)

        results = ConnectionDataService.find_contacts(
            person_id=int(person_id),
            start_date=start_date,
            end_date=end_date,
            meters=float(distance)
        )

        connection_list: List[Connection] = [
            ConnectionDataResource.pb2_to_model(connection)
            for connection in results.connections
        ]

        return connection_list

    @staticmethod
    def pb2_to_model(connection) -> Connection:
        location_pb2 = connection.location
        location = Location(id=location_pb2.id,
                            person_id=location_pb2.person_id,
                            wkt_shape=location_pb2.wkt_shape,
                            creation_time=datetime.fromtimestamp(
                                location_pb2.creation_time.seconds)
                            )

        person_pb2 = connection.person
        person = Person(id=person_pb2.id,
                        first_name=person_pb2.first_name,
                        last_name=person_pb2.last_name,
                        company_name=person_pb2.company_name)

        return Connection(person=person, location=location)
