import uuid
from decimal import Decimal
from unittest.mock import MagicMock

import pytest

from entities.entities import Account
from use_cases.accounts.accounts import AccountUseCases
from use_cases.accounts.exceptions import MissingAccountException


class AccountRepositoryMock:
    def create(self, account: Account) -> Account:  # type: ignore
        ...

    def update(self, id: str, account: Account) -> Account:  # type: ignore
        ...

    def delete(self, id: str) -> None:
        ...

    def get_all(self) -> list[Account]:  # type: ignore
        ...

    def get(self, id: str) -> Account:  # type: ignore
        ...


mock = AccountRepositoryMock()


@pytest.fixture(scope="function")
def account_to_be_updated():
    return Account(
        str(uuid.uuid4()),
        user_id=str(uuid.uuid4()),
        name="Main",
        balance=Decimal("0.0"),
    )


def test_create_account_use_case():
    user_id = str(uuid.uuid4())
    account = Account(
        None, user_id=user_id, name="Main", balance=Decimal("0.0")
    )
    expected_account = Account(
        id=str(uuid.uuid4()),
        user_id=user_id,
        name=account.name,
        balance=account.balance,
    )
    mock.create = MagicMock(return_value=expected_account)
    use_cases = AccountUseCases(mock)
    account_created = use_cases.create_account(account)
    assert account_created.id is not None
    assert account_created.id == expected_account.id
    assert account_created.name == expected_account.name
    assert account_created.balance == expected_account.balance
    assert account_created.user_id == expected_account.user_id


def test_update_account_use_case():
    user_id = str(uuid.uuid4())
    account_to_be_updated = Account(
        str(uuid.uuid4()), user_id=user_id, name="Main", balance=Decimal("0.0")
    )
    expected_account = Account(
        id=account_to_be_updated.id,
        user_id=user_id,
        name="My CC",
        balance=Decimal("100.0"),
    )
    mock.update = MagicMock(return_value=expected_account)
    use_cases = AccountUseCases(mock)
    account_updated = use_cases.update_account(
        account_to_be_updated.id, expected_account
    )
    assert account_updated.id == expected_account.id
    assert account_updated.name == expected_account.name
    assert account_updated.balance == expected_account.balance
    assert account_updated.user_id == expected_account.user_id


def test_update_account_use_case_when_account_does_not_exist(
    account_to_be_updated,
):
    mock.update = MagicMock(side_effect=MissingAccountException)
    use_cases = AccountUseCases(mock)
    with pytest.raises(MissingAccountException):
        use_cases.update_account(
            account_to_be_updated.id, account_to_be_updated
        )


def test_update_account_use_case_when_user_does_not_exist(
    account_to_be_updated,
):
    # TODO Implement this test case after User use cases are doen due to a MissingUserException
    ...


def test_delete_account_when_account_does_not_exist():
    mock.delete = MagicMock(side_effect=MissingAccountException)
    use_cases = AccountUseCases(mock)
    with pytest.raises(MissingAccountException):
        use_cases.delete_account(str(uuid.uuid4()))


def test_get_all_accounts_use_case(account_to_be_updated):
    expected_accounts = [account_to_be_updated]
    mock.get_all = MagicMock(return_value=expected_accounts)
    use_cases = AccountUseCases(mock)
    accounts = use_cases.get_all()
    assert len(accounts) == len(expected_accounts)


def test_get_account_use_case(account_to_be_updated):
    expected_account = account_to_be_updated
    mock.get = MagicMock(return_value=expected_account)
    use_cases = AccountUseCases(mock)
    account = use_cases.get(account_to_be_updated.id)
    assert account == expected_account


def test_get_missing_account_use_case(account_to_be_updated):
    mock.get = MagicMock(side_effect=MissingAccountException)
    use_cases = AccountUseCases(mock)
    with pytest.raises(MissingAccountException):
        use_cases.get(account_to_be_updated.id)
