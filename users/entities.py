from dataclasses import dataclass


@dataclass(frozen=True)
class User:
    name: str
    email: str
    password: str
    id: str | None = None
