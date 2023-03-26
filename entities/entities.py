from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
from typing import Optional


@dataclass(frozen=True)
class Tag:
    name: str
    color: Optional[str] = None


@dataclass(frozen=True)
class Record:
    description: str
    value: Decimal
    date: datetime
    tags: Optional[list[Tag]] = None


@dataclass(frozen=True)
class Account:
    name: str
    balance: Decimal
    records: list[Record]


@dataclass(frozen=True)
class Expense(Record):
    pass


@dataclass(frozen=True)
class Income(Record):
    pass


@dataclass(frozen=True)
class Transference:
    origin_account: Account
    destination_account: Account
    description: str
    value: Decimal
    date: datetime
