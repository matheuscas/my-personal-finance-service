from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class User:
    name: str
    email: str
    password: str
    id: Optional[str] = None
