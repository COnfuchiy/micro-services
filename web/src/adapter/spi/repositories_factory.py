from web.src.adapter.spi.repositories.pps_repository import PpsRepository


class RepositoriesFactory:

    def __init__(self) -> None:
        self._repositories: dict = {
            "pps_repository": PpsRepository(),
        }

    def get_repository(self, repository_name: str):
        if repository_name in self._repositories:
            return self._repositories[repository_name]
        else:
            raise Exception("Repository does not exist")
