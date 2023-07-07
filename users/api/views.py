from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.exceptions import MethodNotAllowed, bad_request

from users.entities import User
from users.models import UserRepository
from users.use_cases.exceptions import (
    ExistingUserException,
    UserNotFoundException,
)
from users.use_cases.users import UserUseCases


class UsersView(APIView):
    class CreateSerializer(serializers.Serializer):
        first_name = serializers.CharField()
        last_name = serializers.CharField()
        email = serializers.EmailField()
        password = serializers.CharField()

    class UpdateSerializer(serializers.Serializer):
        first_name = serializers.CharField(required=False)
        last_name = serializers.CharField(required=False)

    class OutputSerializer(serializers.Serializer):
        first_name = serializers.CharField()
        last_name = serializers.CharField()
        email = serializers.EmailField()
        id = serializers.CharField()

    use_cases = UserUseCases(user_repository=UserRepository())

    def post(self, request):
        data = self.CreateSerializer(data=request.data)
        data.is_valid(raise_exception=True)

        try:
            created_user = self.use_cases.create_user(
                User(
                    first_name=data.validated_data["first_name"],
                    last_name=data.validated_data["last_name"],
                    email=data.validated_data["email"],
                    password=data.validated_data["password"],
                )
            )
        except ExistingUserException as e:
            return Response(
                {"message": e.msg, "extra": {}},
                status=status.HTTP_409_CONFLICT,
            )

        return Response(
            self.OutputSerializer(created_user).data,
            status=status.HTTP_201_CREATED,
        )

    def get(self, request, id=None):
        email = request.query_params.get("email")
        if email:
            try:
                return Response(
                    self.OutputSerializer(
                        self.use_cases.get_user_by_email(email)
                    ).data,
                    status=status.HTTP_200_OK,
                )
            except UserNotFoundException as e:
                return Response(
                    {"message": e.msg, "extra": {}},
                    status=status.HTTP_404_NOT_FOUND,
                )
        elif id:
            try:
                return Response(
                    self.OutputSerializer(self.use_cases.get_user(id)).data,
                    status=status.HTTP_200_OK,
                )
            except UserNotFoundException as e:
                return Response(
                    {"message": e.msg, "extra": {}},
                    status=status.HTTP_404_NOT_FOUND,
                )

        raise MethodNotAllowed(method="GET")

    def put(self, request, id=None):
        serializer = self.UpdateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        if not serializer.validated_data:
            return Response(
                {
                    "message": "Validation error",
                    "extra": {
                        "fields": {
                            "fields": ["You must send at least one field."]
                        }
                    },
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        if id:
            try:
                user = {
                    **serializer.data,
                    "password": "",
                    "email": "",
                }
                return Response(
                    self.OutputSerializer(
                        self.use_cases.update_user(id, User(**user))
                    ).data,
                    status=status.HTTP_200_OK,
                )
            except UserNotFoundException as e:
                return Response(
                    {"message": e.msg, "extra": {}},
                    status=status.HTTP_404_NOT_FOUND,
                )

        raise bad_request(request, Exception)
