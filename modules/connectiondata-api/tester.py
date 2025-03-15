import grpc
import os
import sys

from datetime import datetime
from google.protobuf.timestamp_pb2 import Timestamp

from app.udaconnect.proto.connection_data_pb2_grpc import ConnectionDataServiceStub
from app.udaconnect.proto.connection_data_pb2 import SearchMessage


def validate_args(args):

    args_len = len(args)

    if args_len not in range(3, 5):
        print(f"Number of arguments is invalid: Expected 3 ~ 4 / got {args_len}")
        print("Usage: ")
        print("\t$ python tester.py 6 2020-01-01 2020-06-30 [5]\n")

        raise ValueError("Invalid number of arguments")

    person_id_arg = int(args[0])
    start_arg = args[1].split("-")
    end_arg = args[2].split("-")
    distance_arg = None

    if args_len == 4:
        distance_arg = float(args[3])

    if len(start_arg) != 3:
        raise ValueError(f"Start date is invalid: {sys.argv[2]}")

    if len(end_arg) != 3:
        raise ValueError(f"Start date is invalid: {sys.argv[2]}")

    return person_id_arg, start_arg, end_arg, distance_arg


if __name__ == '__main__':

    grpc_host = os.environ.get('GRPC_HOST') or 'localhost:30003'

    channel = grpc.insecure_channel(grpc_host)
    stub = ConnectionDataServiceStub(channel)

    person_id, start_date, end_date, distance = validate_args(sys.argv[1:])

    t_start = datetime(year=int(start_date[0]), month=int(start_date[1]), day=int(start_date[2]))
    t_end = datetime(year=int(end_date[0]), month=int(end_date[1]), day=int(end_date[2]))

    ts_start = Timestamp(seconds=int(t_start.timestamp()))
    ts_end = Timestamp(seconds=int(t_end.timestamp()))

    search_msg = SearchMessage(person_id=person_id,
                               start_date=ts_start,
                               end_date=ts_end,
                               meters=distance)

    print(f"Search Message send to {grpc_host} -> {search_msg}")
    response = stub.FindContacts(search_msg)

    print(f"Response: {response}")
