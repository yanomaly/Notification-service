from abc import ABC, abstractmethod
from typing import Generic, Optional, TypeVar

T = TypeVar("T")


class DBPort(Generic[T], ABC):

    @abstractmethod
    def get_session(self): ...

    @abstractmethod
    def commit_session(self, session): ...

    @abstractmethod
    def rollback_session(self, session): ...

    @abstractmethod
    def close_session(self, session): ...

    @abstractmethod
    def get_by_id(self, session, db: str, table: str, id: int | str) -> Optional[T]: ...

    @abstractmethod
    def insert(self, session, db: str, table: str, record: T) -> T: ...

    @abstractmethod
    def update(self, session, db: str, table: str, record: T) -> T: ...

    @abstractmethod
    def delete(self, session, db: str, table: str, id: int | str) -> None: ...
