from dataclasses import dataclass


@dataclass(frozen=True)
class User:
    first_name: str
    last_name: str
    email: str
    password: str
    id: str | None = None
