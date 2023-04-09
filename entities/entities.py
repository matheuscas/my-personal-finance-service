from dataclasses import dataclass, field
from datetime import datetime
from decimal import Decimal
from enum import Enum
from typing import Optional


@dataclass(frozen=True)
class Tag:
    name: str
    color: Optional[str] = None


class RecordType(Enum):
    EXPENSE = 0
    INCOME = 1


@dataclass(frozen=True)
class Account:
    name: str
    balance: Decimal


@dataclass(frozen=True)
class Record:
    id: str | None
    description: str
    value: Decimal
    date: datetime
    account: Account
    type: RecordType
    tags: Optional[list[Tag]] = None


@dataclass(frozen=True)
class Expense(Record):
    type: RecordType = field(default=RecordType.EXPENSE)


@dataclass(frozen=True)
class Income(Record):
    type: RecordType = field(default=RecordType.INCOME)


@dataclass(frozen=True)
class Transference:
    origin_account: Account
    destination_account: Account
    description: str
    value: Decimal
    date: datetime
