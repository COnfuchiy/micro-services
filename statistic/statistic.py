import unittest
from unittest.mock import MagicMock

import pandas as pd

from statistic.src.data_handler import PandasDataHandler
from statistic.src.data_source import PandasDataSource
from statistic.src.data_validator import PandasDataValidator
from statistic.src.pps_statistic_service import PpsStatisticService
from statistic.grpc_api.pps_pb2 import (
    TotalStatisticRequest,
    FacultiesListRequest
)


class PppStatisticTest(unittest.TestCase):
    def test_invalid_data_source(self):
        ds = PandasDataSource()
        dv = PandasDataValidator(ds)
        dh = PandasDataHandler(ds, dv)

        dv.validate = MagicMock(return_value=False)

        with self.assertRaises(Exception) as context:
            test_pps = PpsStatisticService(dh)

    def test_total_statistic(self):
        class TestTotalStatisticDataSource(PandasDataSource):
            @property
            def ds(self):
                return pd.DataFrame(['Сергеев Александр Сергеевич','Барабанов Виктор Геннадьевич'], columns=['Ф.И.О.'])
        ds = TestTotalStatisticDataSource()
        dv = PandasDataValidator(ds)
        dh = PandasDataHandler(ds, dv)

        dv.validate = MagicMock(return_value=True)
        test_pps = PpsStatisticService(dh)

        self.assertEqual(test_pps.TotalStatistic(TotalStatisticRequest(), None).employee_count, 2)

    def test_faculties_list(self):
        faculties = ['Факультет автоматизированных систем, транспорта и вооружений','Факультет технологии пищевых производств']

        class TestFacultiesListDataSource(PandasDataSource):
            @property
            def ds(self):
                return pd.DataFrame(faculties, columns=['Факультет'])

        ds = TestFacultiesListDataSource()
        dv = PandasDataValidator(ds)
        dh = PandasDataHandler(ds, dv)

        dv.validate = MagicMock(return_value=True)
        test_pps = PpsStatisticService(dh)

        self.assertEqual(test_pps.FacultiesList(FacultiesListRequest(), None), faculties)


if __name__ == '__main__':
    unittest.main()
