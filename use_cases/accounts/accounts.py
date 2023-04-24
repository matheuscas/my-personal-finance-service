from typing import Protocol

from entities.entities import Account


class AccountRepository(Protocol):
    def create(self, account: Account) -> Account:
        ...

    def update(self, id: str, account: Account) -> Account:
        ...

    def delete(self, id: str) -> None:
        ...

    def get_all(self) -> list[Account]:
        ...

    def get(self, id: str) -> Account:
        ...


class AccountUseCases:
    def __init__(self, account_repository: AccountRepository):
        self.account_repository = account_repository

    def create_account(self, account: Account) -> Account:
        return self.account_repository.create(account)

    def update_account(self, id: str, account: Account) -> Account:
        return self.account_repository.update(id, account)

    def delete_account(self, id: str) -> None:
        self.account_repository.delete(id)

    def get_all(self) -> list[Account]:
        return self.account_repository.get_all()

    def get(self, id: str) -> Account:
        return self.account_repository.get(id)
