import traceback
from typing import Union, List

from fastapi import APIRouter, Query
from fastapi_injector import Injected

from web.src.adapter.api.pps.pps_mappers import PpsStatisticTypesMapper
from web.src.adapter.spi.repositories_factory import RepositoriesFactory
from web.src.adapter.api.shared.api_error_handling import ApiErrorHandling
from web.src.application.repositories.pps_repository_abstract import PpsRepositoryAbstract
from web.src.application.usecases.get_total_statistic_usecase import GetTotalStatisticUseCase
from web.src.application.usecases.get_faculty_statistic_usecase import GetFacultyStatisticUseCase
from web.src.application.usecases.get_chair_statistic_usecase import GetChairStatisticUseCase
from web.src.application.usecases.get_chair_list_usecase import GetChairsListUseCase
from web.src.application.usecases.get_faculties_list_usecase import GetFacultiesListUseCase

from google.protobuf.json_format import MessageToDict

router = APIRouter()

from web.src.infrastructure.pps_pb2 import (
    StatisticResponse,
    ChairsListResponse,
    FacultiesListResponse,
)


@router.get("/statistic")
async def get_total_statistic(types:Union[List[str], None] = Query(default=[]),
                              factory: RepositoriesFactory = Injected(RepositoriesFactory)):
    try:
        statistic_types: list = PpsStatisticTypesMapper().to_entity(types)
        pps_repository :PpsRepositoryAbstract = factory.get_repository("pps_repository")
        get_total_statistic_usecase = GetTotalStatisticUseCase(
            repository=pps_repository,
            statistic_type=statistic_types
        )
        total_statistic:StatisticResponse = get_total_statistic_usecase.execute()

        return MessageToDict(total_statistic)
    except Exception as exception:
        print(traceback.print_exc())
        raise ApiErrorHandling.http_error("Unexpected error getting total statistic", exception)


@router.get("/statistic/{faculty}/")
async def get_faculty_statistic(faculty:str,
                                types:Union[List[str], None] = Query(default=[]),
                                factory: RepositoriesFactory = Injected(RepositoriesFactory)):
    try:
        statistic_types: list = PpsStatisticTypesMapper().to_entity(types)
        pps_repository :PpsRepositoryAbstract = factory.get_repository("pps_repository")
        get_faculty_statistic_usecase = GetFacultyStatisticUseCase(
            repository=pps_repository,
            statistic_type=statistic_types,
            faculty=faculty
        )
        faculty_statistic: StatisticResponse = get_faculty_statistic_usecase.execute()
        return MessageToDict(faculty_statistic)

    except Exception as exception:
        print(traceback.print_exc())
        raise ApiErrorHandling.http_error("Unexpected error getting faculty statistic", exception)

@router.get("/statistic/{faculty}/{chair}/")
async def get_chair_statistic(faculty:str, chair:str,
                              types: Union[List[str], None] = Query(default=[]),
                              factory: RepositoriesFactory = Injected(RepositoriesFactory)
                              ):
    try:
        statistic_types: list = PpsStatisticTypesMapper().to_entity(types)
        pps_repository: PpsRepositoryAbstract = factory.get_repository("pps_repository")
        get_chair_statistic_usecase = GetChairStatisticUseCase(
            repository=pps_repository,
            statistic_type=statistic_types,
            faculty=faculty,
            chair=chair
        )
        chair_statistic: StatisticResponse = get_chair_statistic_usecase.execute()
        return MessageToDict(chair_statistic)

    except Exception as exception:
        print(traceback.print_exc())
        raise ApiErrorHandling.http_error("Unexpected error getting chair statistic", exception)

@router.get("/chairs/{faculty}")
async def get_chair_list(faculty:str,
                         factory: RepositoriesFactory = Injected(RepositoriesFactory)):
    try:
        pps_repository: PpsRepositoryAbstract = factory.get_repository("pps_repository")
        get_chairs_list_usecase = GetChairsListUseCase(
            repository=pps_repository,
            faculty=faculty
        )
        chair_list: ChairsListResponse = get_chairs_list_usecase.execute()
        return MessageToDict(chair_list)

    except Exception as exception:
        raise ApiErrorHandling.http_error("Unexpected error getting chair list", exception)

@router.get("/faculties")
async def get_faculties_list(factory: RepositoriesFactory = Injected(RepositoriesFactory)):
    try:
        pps_repository: PpsRepositoryAbstract = factory.get_repository("pps_repository")
        get_faculties_list_usecase = GetFacultiesListUseCase(
            repository=pps_repository,
        )
        faculties_list: FacultiesListResponse = get_faculties_list_usecase.execute()
        return MessageToDict(faculties_list)

    except Exception as exception:
        raise ApiErrorHandling.http_error("Unexpected error getting faculties list", exception)
