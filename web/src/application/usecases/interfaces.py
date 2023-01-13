from abc import ABC, abstractmethod
from typing import Generic, TypeVar

Entity = TypeVar("Entity")


class GenericUseCase(ABC, Generic[Entity]):
    @abstractmethod
    def execute(self) -> Entity:
        """Execute a use case & return an generic type"""