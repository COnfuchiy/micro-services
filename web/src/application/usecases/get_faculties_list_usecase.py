import traceback

from web.src.application.repositories.pps_repository_abstract import PpsRepositoryAbstract
from web.src.application.usecases.interfaces import GenericUseCase
from web.src.application.utils.error_handling_utils import ErrorHandlingUtils
from web.src.infrastructure.pps_pb2 import (
    FacultiesListResponse
)


class GetFacultiesListUseCase(GenericUseCase):

    def __init__(self, repository: PpsRepositoryAbstract) -> None:
        self._repository = repository

    def execute(self) -> FacultiesListResponse:
        try:
            return self._repository.get_faculties_list()
        except Exception as exception:
            print(traceback.print_exc())
            raise ErrorHandlingUtils.application_error("Cannot get all cat facts", exception)
