from django.urls import path
from .views import RegisterApiView, LoginApiView, ProfileApiView

urlpatterns = [
    path('register/', RegisterApiView.as_view()),
    path('login/', LoginApiView.as_view()),
    path('profile/', ProfileApiView.as_view()),
]
