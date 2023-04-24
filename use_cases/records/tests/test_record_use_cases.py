import uuid
from datetime import datetime
from decimal import Decimal
from unittest.mock import MagicMock

import pytest

from entities.entities import Account, Expense, Record, RecordType, Tag
from use_cases.records.exceptions import (
    RecordMissingIdException,
    RecordNotFoundException,
)
from use_cases.records.records import RecordUseCases
from use_cases.tags.exceptions import MissingTagException


class RecordServiceProtocolMock:
    def create(self, record: Record) -> Record:  # type: ignore
        ...

    def update(self, record: Record) -> Record:  # type: ignore
        ...

    def delete(self, id: str) -> None:
        ...

    def get(self, id: str) -> Record:  # type: ignore
        ...


mock = RecordServiceProtocolMock()


@pytest.fixture(scope="function")
def account():
    return Account(
        str(uuid.uuid4()),
        user_id=str(uuid.uuid4()),
        name="Main",
        balance=Decimal("0.0"),
    )


def test_create_record_with_tags_use_case(account):
    tags = [Tag("Bills"), Tag("House")]
    record = Expense(
        None,
        "Water",
        Decimal("10.34"),
        datetime(2023, 4, 8),
        tags=tags,
        account=account,
    )
    expected_record = Record(
        str(uuid.uuid4()),
        "Water",
        Decimal("10.34"),
        datetime(2023, 4, 8),
        tags=tags,
        type=RecordType.EXPENSE,
        account=account,
    )
    mock.create = MagicMock(return_value=expected_record)
    use_cases = RecordUseCases(mock)
    record_created = use_cases.create_record(record)
    assert record_created.id is not None
    assert record_created.description == expected_record.description
    assert record_created.date == expected_record.date
    assert record_created.type == expected_record.type
    assert record_created.tags == expected_record.tags


def test_create_record_without_tags_use_case(account):
    record = Expense(
        None, "Water", Decimal("10.34"), datetime(2023, 4, 8), account=account
    )
    expected_record = Record(
        str(uuid.uuid4()),
        "Water",
        Decimal("10.34"),
        datetime(2023, 4, 8),
        type=RecordType.EXPENSE,
        account=account,
    )
    mock.create = MagicMock(return_value=expected_record)
    use_cases = RecordUseCases(mock)
    record_created = use_cases.create_record(record)
    assert record_created.id is not None
    assert record_created.description == expected_record.description
    assert record_created.date == expected_record.date
    assert record_created.type == expected_record.type
    assert record_created.tags == expected_record.tags
    assert record_created.tags is None


def test_update_record_raising_missing_id_exception_use_case(account):
    record_to_be_updated = Expense(
        None, "Water", Decimal("10.34"), datetime(2023, 4, 8), account=account
    )
    mock.update = MagicMock(side_effect=RecordMissingIdException)
    use_cases = RecordUseCases(mock)
    with pytest.raises(RecordMissingIdException) as missingIdExc:
        use_cases.update_record(record_to_be_updated)
        assert (
            str(missingIdExc)
            == "records's id is missing. Can' update a records without it"
        )


def test_update_record_raising_record_not_found_exception_use_case(account):
    record_to_be_updated = Expense(
        None, "Water", Decimal("10.34"), datetime(2023, 4, 8), account=account
    )
    mock.update = MagicMock(side_effect=RecordNotFoundException)
    use_cases = RecordUseCases(mock)
    with pytest.raises(RecordNotFoundException) as exc:
        use_cases.update_record(record_to_be_updated)
        assert str(exc) == "records not found"


def test_update_record_raising_missing_tag_use_case(account):
    missing_tag = Tag("Car")
    record_to_be_updated = Expense(
        "123",
        "Water",
        Decimal("10.34"),
        datetime(2023, 4, 8),
        account=account,
        tags=[missing_tag],
    )
    mock.update = MagicMock(side_effect=MissingTagException)
    use_cases = RecordUseCases(mock)
    with pytest.raises(MissingTagException) as exc:
        use_cases.update_record(record_to_be_updated)
        assert str(exc) == "Tag does not exist"


def test_update_record_raising_missing_account_use_case():
    # TODO implement this test after account is implemented
    ...


def test_update_record_use_case(account):
    tags = [Tag("Bills"), Tag("House")]
    record_id = str(uuid.uuid4())
    record = Expense(
        record_id,
        "Water",
        Decimal("10.34"),
        datetime(2023, 4, 8),
        tags=tags,
        account=account,
    )
    expected_record = Record(
        record_id,
        "Water",
        Decimal("10.34"),
        datetime(2023, 4, 8),
        tags=tags,
        type=RecordType.EXPENSE,
        account=account,
    )
    mock.update = MagicMock(return_value=expected_record)
    use_cases = RecordUseCases(mock)
    record_created = use_cases.update_record(record)
    assert record_created.id is not None
    assert record_created.description == expected_record.description
    assert record_created.date == expected_record.date
    assert record_created.type == expected_record.type
    assert record_created.tags == expected_record.tags


def test_delete_record_use_case():
    record_id = str(uuid.uuid4())
    mock.delete = MagicMock(return_value=None)
    use_cases = RecordUseCases(mock)
    use_cases.delete_record(record_id)
    assert mock.delete.call_count == 1


def test_delete_record_raising_missing_record_exception_use_case():
    record_id = str(uuid.uuid4())
    mock.delete = MagicMock(side_effect=RecordNotFoundException)
    use_cases = RecordUseCases(mock)
    with pytest.raises(RecordNotFoundException) as exc:
        use_cases.delete_record(record_id)
        assert str(exc) == "record not found"


def test_get_record_use_case(account):
    record_id = str(uuid.uuid4())
    record = Expense(
        record_id,
        "Water",
        Decimal("10.34"),
        datetime(2023, 4, 8),
        account=account,
    )
    mock.get = MagicMock(return_value=record)
    use_cases = RecordUseCases(mock)
    record_created = use_cases.get(record_id)
    assert record_created.id is not None
    assert record_created.description == record.description
    assert record_created.date == record.date
    assert record_created.type == record.type
    assert record_created.tags == record.tags


def test_get_record_raising_missing_record_exception_use_case():
    record_id = str(uuid.uuid4())
    mock.get = MagicMock(side_effect=RecordNotFoundException)
    use_cases = RecordUseCases(mock)
    with pytest.raises(RecordNotFoundException) as exc:
        use_cases.get(record_id)
        assert str(exc) == "record not found"
