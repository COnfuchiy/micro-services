from abc import ABC, abstractmethod
from data_source import DataSource
import pandas as pd


class DataValidator(ABC):

    @abstractmethod
    def _after_validation(self):
        pass

    @abstractmethod
    def _before_validation(self):
        pass

    @abstractmethod
    def validate(self) -> bool:
        pass

    @abstractmethod
    def __init__(self, ds: DataSource):
        self._ds = ds
        self._errors = []

    @property
    @abstractmethod
    def errors(self) -> list:
        pass


class PandasDataValidator(DataValidator):
    _necessary_columns = [
        'Ф.И.О.',
        'Факультет',
        'Кафедра',
        'Дата рождения',
        'Дата приема на работу',
        'Должность',
        'Количество ставки',
        'Занятость',
        'Ученая степень',
        'Ученое звание',
        'Монографии',
        'Учебники',
        'Учебные пособия с грифом',
        'ВАК',
        'Патенты',
        'Лицензии',
        'Доп. показатели',
        'Scopus/WoS-2017',
        'Scopus/WoS-2018',
        'Scopus/WoS-2019',
        'НИР',
        'Образовательные услуги',
    ]

    _fill_null_columns = {
        'Кафедра': 'Без кафедры (декан факульта)',
        'Ученая степень': 'Без ученой степени',
        'Ученое звание': 'Без ученого звания',
        'Патенты': 0,
        'Лицензии': 0,
        'Доп. показатели': 0,
        'НИР': .0,
        'Образовательные услуги': .0,
    }

    _columns_types = {
        'Количество ставки': float,
        'НИР': float,
        'Образовательные услуги': float,
    }

    def _before_validation(self):
        pass

    def __init__(self, ds: DataSource):
        super().__init__(ds)

    def _after_validation(self):
        self._ds.ds.fillna(self._fill_null_columns, inplace=True)
        for column in self._columns_types:
            self._ds.ds[column].astype(self._columns_types[column])

    def validate(self) -> bool:
        self._before_validation()
        if not isinstance(self._ds.ds, pd.DataFrame):
            self._errors.append(f'{self._ds.path} is not a pandas DataFrame')
            return False
        count_row, count_column = self._ds.ds.shape
        if count_column == 0:
            self._errors.append(f'{self._ds.path} does not contain columns')
            return False
        if count_row == 0:
            self._errors.append(f'{self._ds.path} is empty')
            return False
        for expected_col in self._necessary_columns:
            if not expected_col in self._ds.ds.columns:
                self._errors.append(f'{self._ds.path} does not contain column {expected_col}')
        if len(self._errors):
            return False
        self._after_validation()
        return True

    @property
    def errors(self) -> list:
        return self._errors
