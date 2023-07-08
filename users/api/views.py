from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.exceptions import MethodNotAllowed
from drf_spectacular.utils import (
    extend_schema,
    OpenApiParameter,
    OpenApiExample,
    OpenApiResponse,
)

from users.entities import User
from users.models import UserRepository
from users.use_cases.exceptions import (
    ExistingUserException,
    UserNotFoundException,
)
from users.use_cases.users import UserUseCases


class OutputSerializer(serializers.Serializer):
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    email = serializers.EmailField()
    id = serializers.CharField()


class StandardErrorSerializer(serializers.Serializer):
    message = serializers.CharField()
    extra = serializers.DictField()


class UsersCreation(APIView):
    class CreationSerializer(serializers.Serializer):
        first_name = serializers.CharField()
        last_name = serializers.CharField()
        email = serializers.EmailField()
        password = serializers.CharField()

    serializer = CreationSerializer

    use_cases = UserUseCases(user_repository=UserRepository())

    @extend_schema(
        request=serializer,
        responses={
            "201": OutputSerializer,
            "409": OpenApiResponse(
                description=ExistingUserException.msg,
                response=StandardErrorSerializer,
                examples=[
                    OpenApiExample(
                        "Default answer",
                        value={
                            "message": ExistingUserException.msg,
                            "extra": {},
                        },
                    )
                ],
            ),
        },
        methods=["POST"],
    )
    def post(self, request):
        data = self.serializer(data=request.data)
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
            OutputSerializer(created_user).data,
            status=status.HTTP_201_CREATED,
        )


class UsersDetail(APIView):
    class UpdateSerializer(serializers.Serializer):
        first_name = serializers.CharField(required=False)
        last_name = serializers.CharField(required=False)

    use_cases = UserUseCases(user_repository=UserRepository())

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name="id",
                required=True,
                location=OpenApiParameter.PATH,
                description="The ID of the user",
            ),
        ],
        responses={
            "200": OutputSerializer,
            "404": OpenApiResponse(
                description="User not found",
                response=StandardErrorSerializer,
                examples=[
                    OpenApiExample(
                        "Default response",
                        value={
                            "message": UserNotFoundException.msg,
                            "extra": {},
                        },
                    )
                ],
            ),
        },
        methods=["GET"],
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
                    OutputSerializer(self.use_cases.get_user(id)).data,
                    status=status.HTTP_200_OK,
                )
            except UserNotFoundException as e:
                return Response(
                    {"message": e.msg, "extra": {}},
                    status=status.HTTP_404_NOT_FOUND,
                )

        raise MethodNotAllowed(method="GET")

    @extend_schema(
        request=UpdateSerializer,
        responses={
            "200": OutputSerializer,
            "404": OpenApiResponse(
                description="User not found",
                response=StandardErrorSerializer,
                examples=[
                    OpenApiExample(
                        "User not found",
                        value={
                            "message": UserNotFoundException.msg,
                            "extra": {},
                        },
                    )
                ],
            ),
            "400": OpenApiResponse(
                description="Validation error",
                response=StandardErrorSerializer,
                examples=[
                    OpenApiExample(
                        "Validation error",
                        value={
                            "message": "Validation error",
                            "extra": {
                                "fields": {
                                    "fields": [
                                        "You must send at least one field."
                                    ]
                                }
                            },
                        },
                    )
                ],
            ),
        },
        methods=["PUT"],
    )
    def put(self, request, id):
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

        try:
            user = {
                **serializer.data,
                "password": "",
                "email": "",
            }
            return Response(
                OutputSerializer(
                    self.use_cases.update_user(id, User(**user))
                ).data,
                status=status.HTTP_200_OK,
            )
        except UserNotFoundException as e:
            return Response(
                {"message": e.msg, "extra": {}},
                status=status.HTTP_404_NOT_FOUND,
            )
