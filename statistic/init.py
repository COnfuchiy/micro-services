import os, sys

from statistic.src.data_handler import PandasDataHandler
from statistic.src.data_source import PandasDataSource
from statistic.src.data_validator import PandasDataValidator

path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(path+'/grpc_api')
sys.path.append(path+'/src')

from concurrent import futures
import grpc
import grpc_api
from src.pps_statistic_service import PpsStatisticService

server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
ds = PandasDataSource()
dv = PandasDataValidator(ds)
dh = PandasDataHandler(ds, dv)
pps_statistic = PpsStatisticService(dh)
grpc_api.pps_pb2_grpc.add_PpsStatisticServicer_to_server(pps_statistic,server)
server.add_insecure_port("[::]:50051")
server.start()
server.wait_for_termination()

