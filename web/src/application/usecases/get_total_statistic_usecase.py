from web.src.application.repositories.pps_repository_abstract import PpsRepositoryAbstract
from web.src.application.usecases.interfaces import GenericUseCase
from web.src.application.utils.error_handling_utils import ErrorHandlingUtils
from web.src.infrastructure.pps_pb2 import (
    StatisticResponse
)


class GetTotalStatisticUseCase(GenericUseCase):

    def __init__(self, repository: PpsRepositoryAbstract, statistic_type: list) -> None:
        self._repository = repository
        self._statistic_type = statistic_type

    def execute(self) -> StatisticResponse:
        try:
            return self._repository.get_total_statistic(self._statistic_type)
        except Exception as exception:
            raise ErrorHandlingUtils.application_error("Cannot get all cat facts", exception)

