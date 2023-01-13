import os
import pandas as pd
from abc import ABC, abstractmethod


class DataSource(ABC):

    def __init__(self):
        self._data_path = os.getenv("DATA_PATH", 'data/pps.csv')
        if not self._data_path:
            raise Exception("DATA_PATH is not specify")
        if not self._check_file():
            raise Exception(f"{self._data_path} is invalid")
        self._data_source = self._get_data_source_instance()


    def _check_file(self) -> bool:
        if not os.path.exists(self._data_path) or not os.path.isfile(self._data_path):
            return False
        return True

    @abstractmethod
    def _get_data_source_instance(self) -> object:
        pass

    @property
    def ds(self) -> object:
        return self._data_source

    @property
    def path(self) -> str:
        return self._data_path


class PandasDataSource(DataSource):

    def __init__(self):
        super().__init__()

    def _get_data_source_instance(self) -> pd.DataFrame:
        return pd.read_csv(self._data_path, header=0, sep=';')


