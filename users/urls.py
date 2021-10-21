from django.urls import path

from users.views import KaKaoLoginView 

urlpatterns = [
    path('/login', KaKaoLoginView.as_view()),
]