from abc import ABC, abstractmethod


class PpsRepositoryAbstract(ABC):
    @abstractmethod
    def get_total_statistic(self, statistic_types: list):
        pass

    @abstractmethod
    def get_faculty_statistic(self, faculty:str, statistic_types: list):
        pass

    @abstractmethod
    def get_chair_statistic(self,faculty:str, chair:str, statistic_types: list):
        pass

    @abstractmethod
    def get_chairs_list(self,faculty: str):
        pass

    @abstractmethod
    def get_faculties_list(self):
        pass