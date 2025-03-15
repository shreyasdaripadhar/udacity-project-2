import logging
import grpc
import os
import time

from concurrent import futures

from app.udaconnect.servicers.connectionata_servicer import ConnectionDataServicer
from app.udaconnect.proto.connection_data_pb2_grpc import add_ConnectionDataServiceServicer_to_server


SERVER_PORT = os.environ.get("GRPC_PORT") or 5005

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("udaconnect-dataconnection")


server = grpc.server(futures.ThreadPoolExecutor(max_workers=2))

add_ConnectionDataServiceServicer_to_server(ConnectionDataServicer(), server)

logger.info(f"Server starting on port {SERVER_PORT}")
server.add_insecure_port(f"[::]:{SERVER_PORT}")
server.start()

try:
    while True:
        time.sleep(86400)
except KeyboardInterrupt:
    server.stop(0)
