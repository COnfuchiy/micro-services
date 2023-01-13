import os

import grpc

from web.src.infrastructure.pps_pb2_grpc import PpsStatisticStub

class GrpcPpsStatisticClient(PpsStatisticStub):
    def __init__(self):
        host = os.getenv("RECOMMENDATIONS_HOST", "localhost")
        channel = grpc.insecure_channel(
            f"{host}:50051"
        )
        super().__init__(channel)

