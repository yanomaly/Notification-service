from abc import ABC, abstractmethod
from typing import Optional, TypeVar

T = TypeVar("T")


class DBPort(ABC):
    @abstractmethod
    async def get_by_id(self, id: int | str) -> Optional[T]: ...

    @abstractmethod
    async def insert(self, record: T) -> T: ...

    @abstractmethod
    async def update(self, record: T) -> T: ...

    @abstractmethod
    async def delete(self, id: int | str) -> None: ...
