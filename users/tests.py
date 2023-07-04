import contextlib

import pytest
from django.contrib.auth import get_user_model
from users.entities import User
from users.models import UserRepository
from users.use_cases.exceptions import (
    ExistingUserException,
    UserNotFoundException,
)


# from https://testdriven.io/blog/django-custom-user-model/
@pytest.mark.django_db
def test_create_user():
    User = get_user_model()
    user = User.objects.create_user(email="normal@user.com", password="foo")
    assert user.email == "normal@user.com"
    assert user.is_active
    assert not user.is_staff
    assert not user.is_superuser
    with contextlib.suppress(AttributeError):
        # username is None for the AbstractUser option
        # username does not exist for the AbstractBaseUser option
        assert not user.username
    with pytest.raises(TypeError):
        User.objects.create_user()
    with pytest.raises(TypeError):
        User.objects.create_user(email="")
    with pytest.raises(ValueError):
        User.objects.create_user(email="", password="foo")


@pytest.mark.django_db
def test_create_superuser():
    User = get_user_model()
    admin_user = User.objects.create_superuser(
        email="super@user.com", password="foo"
    )
    assert admin_user.email == "super@user.com"
    assert admin_user.is_active
    assert admin_user.is_staff
    assert admin_user.is_superuser
    with contextlib.suppress(AttributeError):
        # username is None for the AbstractUser option
        # username does not exist for the AbstractBaseUser option
        assert not admin_user.username
    with pytest.raises(ValueError):
        User.objects.create_superuser(
            email="super@user.com", password="foo", is_superuser=False
        )


@pytest.fixture
def repo():
    return UserRepository()


@pytest.fixture
def user():
    return User(
        first_name="John",
        last_name="Smith",
        email="johndoe@me.com",
        password="password",
    )


@pytest.mark.django_db
def test_user_repository_create(repo, user):
    created_user = repo.create(user)
    assert created_user.id is not None
    assert created_user.email == user.email
    assert created_user.first_name == user.first_name
    assert created_user.last_name == user.last_name


@pytest.mark.django_db
def test_user_repository_create_existing_email(repo, user):
    repo.create(user)
    with pytest.raises(ExistingUserException) as e:
        repo.create(user)
        assert str(e.value) == ExistingUserException.msg


@pytest.mark.django_db
def test_user_repository_update(repo, user):
    created_user = repo.create(user)
    changed_user = User(
        first_name="Jane",
        last_name="Smith",
        email="johndoe@me.com",
        password="password2",
    )
    updated_user = repo.update(created_user.id, changed_user)
    assert updated_user.id is not None
    assert updated_user.first_name == changed_user.first_name
    assert updated_user.last_name == changed_user.last_name


@pytest.mark.django_db
def test_user_repository_update_user_not_found(repo, user):
    with pytest.raises(UserNotFoundException) as e:
        repo.update(user.id, user)
        assert str(e.value) == UserNotFoundException.msg


@pytest.mark.django_db
def test_user_repository_get(repo, user):
    created_user = repo.create(user)
    user_found = repo.get(created_user.id)
    assert user_found.id == created_user.id


@pytest.mark.django_db
def test_user_repository_get_user_not_found(repo, user):
    with pytest.raises(UserNotFoundException) as e:
        repo.get(user.id)
        assert str(e.value) == UserNotFoundException.msg
