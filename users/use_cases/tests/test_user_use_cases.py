import hashlib
import uuid
from unittest.mock import MagicMock

import pytest

from users.entities import User
from users.use_cases.exceptions import (
    ExistingUserException,
    UserNotFoundException,
)
from users.use_cases.users import UserUseCases


class UserRepositoryMock:
    def create(self, user: User) -> User:
        ...

    def update(self, id: str, user: User) -> User:
        ...

    def get(self, id: str) -> User:
        ...


mock = UserRepositoryMock()


def test_create_user_use_case():
    user = User(
        first_name="John",
        last_name="Doe",
        email="kJqfR@example.com",
        password="1234",
    )
    expected_user = User(
        id=str(uuid.uuid4()),
        first_name=user.first_name,
        last_name=user.last_name,
        email=user.email,
        password=hashlib.sha256(user.password.encode()).hexdigest(),
    )
    mock.create = MagicMock(return_value=expected_user)
    use_cases = UserUseCases(mock)
    user_created = use_cases.create_user(user)
    assert user_created.id is not None
    assert user_created.email == user.email
    assert user_created.first_name == user.first_name
    assert user_created.last_name == user.last_name
    assert user_created.password != user.password


def test_create_user_existing_email_use_case():
    user = User(
        first_name="John",
        last_name="Doe",
        email="kJqfR@example.com",
        password="1234",
    )
    mock.create = MagicMock(side_effect=ExistingUserException)
    use_cases = UserUseCases(mock)
    with pytest.raises(ExistingUserException):
        use_cases.create_user(user)


def test_update_user_use_case():
    user = User(
        id=str(uuid.uuid4()),
        first_name="Matheus",
        last_name="Cardoso",
        email="kJqfR@example.com",
        password=hashlib.sha256(b"1234").hexdigest(),
    )
    expected_user = User(
        id=user.id,
        first_name=user.first_name,
        last_name=user.last_name,
        email=user.email,
        password=user.password,
    )
    mock.update = MagicMock(return_value=expected_user)
    use_cases = UserUseCases(mock)
    user_updated = use_cases.update_user(user.id, user)
    assert user_updated.id == expected_user.id
    assert user_updated.first_name == expected_user.first_name
    assert user_updated.last_name == expected_user.last_name
    assert user_updated.email == expected_user.email
    assert user_updated.password == expected_user.password


def test_get_user_use_case():
    user = User(
        id=str(uuid.uuid4()),
        first_name="Matheus",
        last_name="Cardoso",
        email="kJqfR@example.com",
        password=hashlib.sha256(b"1234").hexdigest(),
    )
    mock.get = MagicMock(return_value=user)
    use_cases = UserUseCases(mock)
    user_found = use_cases.get_user(user.id)
    assert user_found.id == user.id
    assert user_found.first_name == user.first_name
    assert user_found.last_name == user.last_name
    assert user_found.email == user.email
    assert user_found.password == user.password


def test_user_not_found_use_case():
    mock.get = MagicMock(side_effect=UserNotFoundException)
    use_cases = UserUseCases(mock)
    with pytest.raises(UserNotFoundException):
        use_cases.get_user(str(uuid.uuid4()))
