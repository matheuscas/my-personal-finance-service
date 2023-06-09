from django.contrib.auth.models import AbstractUser
from django.db import IntegrityError, models
from django.utils.translation import gettext_lazy as _

from .entities import User
from .managers import CustomUserManager
from .use_cases.exceptions import ExistingUserException


class CustomUser(AbstractUser):
    """
    from https://testdriven.io/blog/django-custom-user-model/#abstractuser
    """

    username = None
    email = models.EmailField(_("email address"), unique=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email


class UserRepository:
    def create(self, user: User) -> User:
        custom_user = {
            "first_name": user.name,
            "email": user.email,
            "password": user.password,
        }
        try:
            created_user = CustomUser.objects.create_user(**custom_user)
        except IntegrityError as e:
            raise ExistingUserException() from e

        return User(
            name=created_user.first_name,
            email=created_user.email,
            password=created_user.password,
            id=created_user.id,
        )

    def update(self, id: str, user: User) -> User:
        ...

    def get(self, id: str) -> User:
        ...
