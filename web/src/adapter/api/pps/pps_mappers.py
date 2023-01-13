from web.src.application.mappers.api_mapper import ApiMapper, Payload, Entity, Presenter
from web.src.infrastructure.pps_pb2 import StatisticTypes


class PpsStatisticTypesMapper(ApiMapper):

    _statistic_types_query_associate = {
        'age':StatisticTypes.AGE_AVERAGE,
        'experience':StatisticTypes.EXPERIENCE_AVERAGE,
        'position':StatisticTypes.POSITION_COUNT,
        'employment':StatisticTypes.EMPLOYMENT_COUNT,
        'academic':StatisticTypes.ACADEMIC_STATISTIC,
        'significant_publications':StatisticTypes.SIGNIFICANT_PUBLICATIONS_STATISTIC,
        'other_publications':StatisticTypes.OTHER_PUBLICATIONS_STATISTIC,
        'extrabudgetary_funds':StatisticTypes.EXTRABUDGETARY_FUNDS_STATISTIC,
    }

    def to_api(self, entity: Entity) -> Presenter:
        raise Exception("not implemented")

    def to_entity(self, payload: Payload) -> Entity:
        statistic_types_output = []
        for query_param in self._statistic_types_query_associate:
            if query_param in payload:
                statistic_types_output.append(self._statistic_types_query_associate[query_param])
        return statistic_types_output
