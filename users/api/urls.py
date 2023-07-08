from django.urls import path

from .views import UsersDetail, UsersCreation

urlpatterns = [
    path("users/", UsersCreation.as_view()),
    path("users/<int:id>/", UsersDetail.as_view()),
]
