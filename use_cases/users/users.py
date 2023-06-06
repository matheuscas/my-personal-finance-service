from typing import Protocol

from entities.entities import User


class UserRepository(Protocol):
    def create(self, user: User) -> User:
        ...

    def update(self, id: str, user: User) -> User:
        ...

    def get(self, id: str) -> User:
        ...


class UserUseCases:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    def create_user(self, user: User) -> User:
        return self.user_repository.create(user)

    def update_user(self, id: str, user: User) -> User:
        return self.user_repository.update(id, user)

    def get_user(self, id: str) -> User:
        return self.user_repository.get(id)
