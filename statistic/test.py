from src.data_source import PandasDataSource
from src.data_validator import PandasDataValidator
from src.data_handler import PandasDataHandler
from grpc_api.pps_pb2 import StatisticTypes

ds = PandasDataSource()
dv = PandasDataValidator(ds)
dh = PandasDataHandler(ds, dv)
dh.init_data_source()
print(dh.get_all_faculties())
print(dh.get_all_faculty_chairs('Факультет экономики и управления'))
# print(dh.get_total_statistic([
#     StatisticTypes.AGE_AVERAGE,
#     StatisticTypes.EXPERIENCE_AVERAGE,
#     StatisticTypes.POSITION_COUNT,
#     StatisticTypes.EMPLOYMENT_COUNT,
#     StatisticTypes.ACADEMIC_STATISTIC,
#     StatisticTypes.SIGNIFICANT_PUBLICATIONS_STATISTIC,
#     StatisticTypes.OTHER_PUBLICATIONS_STATISTIC,
#     StatisticTypes.EXTRABUDGETARY_FUNDS_STATISTIC,
# ]))