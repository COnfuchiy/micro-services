import grpc

from ..grpc_api.pps_pb2_grpc import PpsStatisticServicer

from data_source import PandasDataSource
from data_validator import PandasDataValidator
from data_handler import PandasDataHandler, DataHandler


class PpsStatisticService(PpsStatisticServicer):

    def __init__(self, dh: DataHandler):

        self._dh = dh
        self._dh.init_data_source()

    def TotalStatistic(self, request, context):
        return self._dh.get_total_statistic(request.statistic_types)


    def FacultiesList(self, request, context):
        return self._dh.get_all_faculties()


    def FacultyStatistic(self, request, context):
        if not request.faculty_name:
            context.abort(grpc.StatusCode.NOT_FOUND, "Faculty not found")
        return self._dh.get_faculty_statistic(request.faculty_name, request.statistic_types)


    def ChairsList(self, request, context):
        if not request.faculty_name:
            context.abort(grpc.StatusCode.NOT_FOUND, "Faculty not found")
        return self._dh.get_all_faculty_chairs(request.faculty_name)


    def ChairStatistic(self, request, context):
        if not request.faculty_name:
            context.abort(grpc.StatusCode.NOT_FOUND, "Faculty not found")
        if not request.chair_name:
            context.abort(grpc.StatusCode.NOT_FOUND, "Chair not found")
        return self._dh.get_chair_statistic(request.faculty_name, request.chair_name, request.statistic_types)
