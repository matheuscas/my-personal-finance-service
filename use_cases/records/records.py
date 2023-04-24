from typing import Protocol

from entities.entities import Record


class RecordsRepository(Protocol):
    def create(self, record: Record) -> Record:
        ...

    def update(self, record: Record) -> Record:
        ...

    def delete(self, id: str) -> None:
        ...

    def get(self, id: str) -> Record:
        ...


class RecordUseCases:
    def __init__(self, service: RecordsRepository):
        self.service = service

    def create_record(self, record: Record) -> Record:
        return self.service.create(record)

    def update_record(self, record: Record) -> Record:
        return self.service.update(record)

    def delete_record(self, id: str):
        self.service.delete(id)

    def get(self, id: str) -> Record:
        return self.service.get(id)
