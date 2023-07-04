from django.contrib.auth.models import AbstractUser
from django.db import IntegrityError, models
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ObjectDoesNotExist

from .entities import User
from .managers import CustomUserManager
from .use_cases.exceptions import ExistingUserException, UserNotFoundException


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
            "first_name": user.first_name,
            "last_name": user.last_name,
            "email": user.email,
            "password": user.password,
        }
        try:
            created_user = CustomUser.objects.create_user(**custom_user)
        except IntegrityError as e:
            raise ExistingUserException() from e

        return User(
            first_name=created_user.first_name,
            last_name=created_user.last_name,
            email=created_user.email,
            password=created_user.password,
            id=created_user.id,
        )

    def update(self, id: str, user: User) -> User:
        user_to_update = self.get(id)
        user_updated = {
            "first_name": user.first_name,
            "last_name": user.last_name,
        }
        CustomUser.objects.update(**user_updated)
        return User(
            first_name=user.first_name,
            last_name=user.last_name,
            email=user_to_update.email,
            password=user_to_update.password,
            id=user_to_update.id,
        )

    def get(self, id: str) -> User:
        try:
            return CustomUser.objects.get(id=id)
        except ObjectDoesNotExist as e:
            raise UserNotFoundException() from e
