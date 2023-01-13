from fastapi_injector import Injected

from web.src.adapter.spi.grpc_clients.grpc_pps_statistic_client import GrpcPpsStatisticClient
from web.src.application.repositories.pps_repository_abstract import PpsRepositoryAbstract
from web.src.infrastructure.pps_pb2 import (
    TotalStatisticRequest,
    FacultiesListRequest,
    FacultyStatisticRequest,
    ChairsListRequest,
    ChairStatisticRequest,
)


class PpsRepository(PpsRepositoryAbstract):
    def __init__(self):
        self._grpc_pps_client = GrpcPpsStatisticClient()

    def get_total_statistic(self, statistic_types: list):
        total_statistic_request = TotalStatisticRequest(statistic_types=statistic_types)
        total_statistic_response = self._grpc_pps_client.TotalStatistic(
            total_statistic_request
        )
        return total_statistic_response


    def get_faculty_statistic(self, faculty: str, statistic_types: list):
        faculty_statistic_request = FacultyStatisticRequest(
            faculty_name=faculty,
            statistic_types=statistic_types
        )
        faculty_statistic_response = self._grpc_pps_client.FacultyStatistic(
            faculty_statistic_request
        )
        return faculty_statistic_response

    def get_chair_statistic(self, faculty: str, chair: str, statistic_types: list):
        chair_statistic_request = ChairStatisticRequest(
            faculty_name=faculty,
            chair_name=chair,
            statistic_types=statistic_types
        )
        chair_statistic_response = self._grpc_pps_client.ChairStatistic(
            chair_statistic_request
        )
        return chair_statistic_response

    def get_chairs_list(self, faculty: str):
        chairs_list_request = ChairsListRequest(
            faculty_name=faculty,
        )
        chairs_list_request = self._grpc_pps_client.ChairsList(
            chairs_list_request
        )
        return chairs_list_request

    def get_faculties_list(self):
        faculties_list_request = FacultiesListRequest()
        faculties_list_response = self._grpc_pps_client.FacultiesList(
            faculties_list_request
        )
        return faculties_list_response

