from abc import ABC, abstractmethod

import numpy as np
import pandas as pd
from dateutil.relativedelta import relativedelta
from data_source import DataSource
from data_validator import DataValidator
from grpc_api.pps_pb2 import (
    StatisticTypes,
    StatisticResponse,
    CountStatistic,
    AverageStatistic,
    ChairsListResponse,
    FacultiesListResponse,
)


class DataHandler(ABC):

    def __init__(self, ds: DataSource, dv: DataValidator):
        self._ds = ds
        self._dv = dv

    def init_data_source(self):
        if not self._dv.validate():
            for error in self._dv.errors:
                print(error)
            raise Exception(f"{self._ds.path} is invalid data source")

    @abstractmethod
    def get_all_faculties(self) -> list:
        pass

    @abstractmethod
    def _get_statistic_from_data(self, data, statistic_types: list)-> object:
        pass

    @abstractmethod
    def get_all_faculty_chairs(self, faculty: str,) -> list:
        pass

    @abstractmethod
    def get_total_statistic(self, statistic_types: list) -> object:
        pass

    @abstractmethod
    def get_faculty_statistic(self, faculty: str, statistic_types: list) -> object:
        pass

    @abstractmethod
    def get_chair_statistic(self, faculty: str, chair: str, statistic_types: list) -> object:
        pass


def calc_age(data):
    data['Дата рождения'] = pd.to_datetime(data['Дата рождения'], dayfirst=True)
    data['age'] = [relativedelta(pd.to_datetime('now'), d).years for d in data['Дата рождения']]


def calc_experience(data):
    data['Дата приема на работу'] = pd.to_datetime(data['Дата приема на работу'], dayfirst=True)
    data['experience'] = [relativedelta(pd.to_datetime('now'), d).years for d in data['Дата приема на работу']]


def create_count_statistic(statistics_dict: dict):
    output = []
    for name in statistics_dict:
        output.append(
            CountStatistic(
                name=name,
                count=statistics_dict[name]
            )
        )
    return output


def create_average_statistic(statistics_dict: dict):
    output = []
    for name in statistics_dict:
        output.append(
            AverageStatistic(
                name=name,
                average=statistics_dict[name]
            )
        )
    return output


def sort_dict_by_desc(statistics_dict: dict):
    return dict(sorted(statistics_dict.items(), key=lambda x: (-x[1], x[0])))


def get_sorted_statistic(data, add_total=False) -> dict:
    sorted_sum_series = sort_dict_by_desc(data.to_dict())
    if add_total:
        sorted_sum_series['Всего'] = np.sum(list(sorted_sum_series.values()))
    return sorted_sum_series


def get_count_and_average_statistic(data) -> tuple[list, list]:
    count_statistic = get_sorted_statistic(data.sum(), True)
    average_statistic = get_sorted_statistic(data.mean(), True)
    return create_count_statistic(count_statistic), \
           create_average_statistic(average_statistic)


class PandasDataHandler(DataHandler):

    def get_total_statistic(self, statistic_types: list) -> StatisticResponse:
        response_data = self._get_statistic_from_data(self._ds.ds, statistic_types)
        return response_data

    def get_faculty_statistic(self, faculty: str, statistic_types: list) -> StatisticResponse:
        response_data = self._get_statistic_from_data(
            self._ds.ds[self._ds.ds['Факультет'] == faculty],
            statistic_types
        )
        response_data.faculty_name = faculty
        return response_data


    def get_chair_statistic(self, faculty: str, chair: str, statistic_types: list) -> StatisticResponse:
        response_data = self._get_statistic_from_data(
            self._ds.ds[
                (self._ds.ds['Факультет'] == faculty) &
                (self._ds.ds['Кафедра'] == chair)],
            statistic_types
        )
        response_data.chair_name = chair
        response_data.faculty_name = faculty
        return response_data

    def get_all_faculties(self) -> FacultiesListResponse:
        faculties = self._ds.ds['Факультет'].unique()
        response_data = FacultiesListResponse(faculties=faculties)
        return response_data

    def _get_statistic_from_data(self, data, statistic_types: list)->StatisticResponse:
        response_data = StatisticResponse()
        response_data.employee_count = len(data['Ф.И.О.'].unique())
        if StatisticTypes.AGE_AVERAGE in statistic_types:
            calc_age(data)
            average_age = data['age'].mean()
            response_data.age_average = int(average_age)
        if StatisticTypes.EXPERIENCE_AVERAGE in statistic_types:
            calc_experience(data)
            experience_average = data['experience'].mean()
            response_data.experience_average = int(experience_average)
        if StatisticTypes.POSITION_COUNT in statistic_types:
            positions = get_sorted_statistic(
                data.groupby(['Должность'])['Должность'].count()
            )

            response_data.positions.extend(create_count_statistic(positions))
        if StatisticTypes.EMPLOYMENT_COUNT in statistic_types:
            employments = get_sorted_statistic(
                data[['Количество ставки', 'Занятость']].groupby(['Занятость'])['Количество ставки'].sum(),
                True
            )
            response_data.employments.extend(create_count_statistic(employments))
        if StatisticTypes.ACADEMIC_STATISTIC in statistic_types:
            academic_degrees = get_sorted_statistic(
                data.groupby(['Ученая степень'])['Ученая степень'].count()
            )

            academic_titles = get_sorted_statistic(
                data.groupby(['Ученое звание'])['Ученое звание'].count()
            )

            response_data.academic_degrees.extend(create_count_statistic(academic_degrees))
            response_data.academic_titles.extend(create_count_statistic(academic_titles))
        if StatisticTypes.SIGNIFICANT_PUBLICATIONS_STATISTIC in statistic_types:
            significant_publications_ds = data[
                ['Монографии', 'Учебники', 'Учебные пособия с грифом', 'ВАК', 'Патенты', 'Лицензии',
                 'Доп. показатели']]

            significant_publications, significant_publications_average = \
                get_count_and_average_statistic(significant_publications_ds)
            response_data.significant_publications.extend(significant_publications)
            response_data.significant_publications_average.extend(significant_publications_average)

        if StatisticTypes.OTHER_PUBLICATIONS_STATISTIC in statistic_types:
            other_publications_ds = data[
                ['Scopus/WoS-2017', 'Scopus/WoS-2018', 'Scopus/WoS-2019']
            ]

            other_publications, other_publications_average = \
                get_count_and_average_statistic(other_publications_ds)
            response_data.other_publications.extend(other_publications)
            response_data.other_publications_average.extend(other_publications_average)
        if StatisticTypes.EXTRABUDGETARY_FUNDS_STATISTIC in statistic_types:
            extrabudgetary_funds_ds = data[['НИР', 'Образовательные услуги']]

            extrabudgetary_funds, extrabudgetary_funds_average = \
                get_count_and_average_statistic(extrabudgetary_funds_ds)
            response_data.extrabudgetary_funds.extend(extrabudgetary_funds)
            response_data.extrabudgetary_funds_average.extend(extrabudgetary_funds_average)

        return response_data


    def get_all_faculty_chairs(self, faculty: str) -> ChairsListResponse:
        chairs = self._ds.ds[self._ds.ds['Факультет'] == faculty]['Кафедра'].unique()
        response_data = ChairsListResponse(chairs=chairs,faculty_name=faculty)
        return response_data

