from typing import Optional

from pymongo import MongoClient
from pymongo.client_session import ClientSession

from domain.message_schemas import MessageForm
from ports.db_port import DBPort


class MongoAdapter(DBPort[MessageForm]):

    def __init__(self, mongo_client: MongoClient):
        self.mongo_client = mongo_client

    def get_session(self) -> ClientSession:
        return self.mongo_client.start_session()

    def commit_session(self, session: ClientSession) -> None:
        session.commit_transaction()

    def rollback_session(self, session: ClientSession) -> None:
        session.abort_transaction()

    def close_session(self, session: ClientSession) -> None:
        session.end_session()

    def insert(
        self, session: ClientSession, db: str, table: str, record: MessageForm
    ) -> MessageForm:
        database = self.mongo_client.get_database(db)
        collection = database.get_collection(table)
        session.start_transaction()
        collection.insert_one(record.dict(), session=session)
        return record

    def get_by_id(
        self, session: ClientSession, db: str, table: str, id: int | str
    ) -> Optional[MessageForm]: ...

    def update(
        self, session: ClientSession, db: str, table: str, record: MessageForm
    ) -> MessageForm: ...

    def delete(
        self, session: ClientSession, db: str, table: str, id: int | str
    ) -> None: ...
