from dataclasses import asdict

import pytest
from rest_framework import status
from rest_framework.test import APIClient

from users.entities import User
from users.models import CustomUser
from users.use_cases.exceptions import ExistingUserException


@pytest.fixture(scope="session")
def api_client():
    return APIClient()


@pytest.mark.parametrize(
    "payload, expected_error",
    [
        (
            {
                "first_name": "John",
                "last_name": "Smith",
                "email": "johndoe@me.com",
            },
            {
                "message": "Validation error",
                "extra": {
                    "fields": {
                        "password": ["This field is required."],
                    }
                },
            },
        ),
        (
            {
                "first_name": "John",
                "last_name": "Smith",
                "password": "password",
            },
            {
                "message": "Validation error",
                "extra": {
                    "fields": {
                        "email": ["This field is required."],
                    }
                },
            },
        ),
        (
            {
                "last_name": "Smith",
                "email": "johndoe@me.com",
                "password": "password",
            },
            {
                "message": "Validation error",
                "extra": {
                    "fields": {
                        "first_name": ["This field is required."],
                    }
                },
            },
        ),
        (
            {
                "first_name": "John",
                "email": "johndoe@me.com",
                "password": "password",
            },
            {
                "message": "Validation error",
                "extra": {
                    "fields": {
                        "last_name": ["This field is required."],
                    }
                },
            },
        ),
    ],
)
def test_required_user_fields(api_client, payload, expected_error):
    response = api_client.post("/api/users/", payload, format="json")
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.data == expected_error


def test_wrong_email_format(api_client):
    response = api_client.post(
        "/api/users/",
        {
            "first_name": "John",
            "last_name": "Smith",
            "email": "johndoeme.com",
            "password": "password",
        },
        format="json",
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.data == {
        "message": "Validation error",
        "extra": {
            "fields": {
                "email": ["Enter a valid email address."],
            }
        },
    }


@pytest.mark.django_db()
def test_existing_user_error(api_client):
    user = User(
        first_name="John",
        last_name="Doe",
        email="johndoe@me.com",
        password="password",
    )
    custom_user = {
        "first_name": user.first_name,
        "last_name": user.last_name,
        "email": user.email,
        "password": user.password,
    }
    CustomUser.objects.create_user(**custom_user)
    response = api_client.post("/api/users/", asdict(user), format="json")
    assert response.status_code == status.HTTP_409_CONFLICT
    assert response.data == {"message": ExistingUserException.msg, "extra": {}}


def test_not_found_user_error():
    ...


def test_user_creation():
    ...


def test_user_update():
    ...


def test_user_read():
    ...
