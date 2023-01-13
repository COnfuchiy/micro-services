from web.src.application.repositories.pps_repository_abstract import PpsRepositoryAbstract
from web.src.application.usecases.interfaces import GenericUseCase
from web.src.application.utils.error_handling_utils import ErrorHandlingUtils
from web.src.infrastructure.pps_pb2 import (
    ChairsListResponse
)


class GetChairsListUseCase(GenericUseCase):

    def __init__(self, repository: PpsRepositoryAbstract, faculty:str) -> None:
        self._repository = repository
        self._faculty = faculty

    def execute(self) -> ChairsListResponse:
        try:
            return self._repository.get_chairs_list(self._faculty)
        except Exception as exception:
            raise ErrorHandlingUtils.application_error("Cannot get all cat facts", exception)
