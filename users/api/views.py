from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework.views import APIView

from users.entities import User
from users.models import UserRepository
from users.use_cases.exceptions import ExistingUserException
from users.use_cases.users import UserUseCases


class UsersView(APIView):
    class InputSerializer(serializers.Serializer):
        name = serializers.CharField()
        email = serializers.EmailField()
        password = serializers.CharField()

    class OutputSerializer(serializers.Serializer):
        name = serializers.CharField()
        email = serializers.EmailField()
        id = serializers.CharField()

    def post(self, request):
        data = self.InputSerializer(data=request.data)
        data.is_valid(raise_exception=True)
        use_cases = UserUseCases(user_repository=UserRepository())

        try:
            created_user = use_cases.create_user(
                User(
                    name=data.validated_data["name"],
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
