import grpc
import logging

from builtins import staticmethod
from google.protobuf.timestamp_pb2 import Timestamp

from app.udaconnect.proto.connection_data_pb2_grpc import ConnectionDataServiceStub
from app.udaconnect.proto.connection_data_pb2 import SearchMessage

logging.basicConfig(level=logging.WARNING)
logger = logging.getLogger("udaconnect-person-svc")


channel = grpc.insecure_channel("udaconnect-connectiondata-api:5005")
stub = ConnectionDataServiceStub(channel)


class ConnectionDataService:

    @staticmethod
    def find_contacts(person_id, start_date, end_date, meters):

        ts_start = Timestamp(seconds=int(start_date.timestamp()))
        ts_end = Timestamp(seconds=int(end_date.timestamp()))

        search_msg = SearchMessage(person_id=person_id,
                                   start_date=ts_start,
                                   end_date=ts_end,
                                   meters=meters)

        response = stub.FindContacts(search_msg)

        return response
