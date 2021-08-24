from django.urls import path

from landing.views import LandingApiView

urlpatterns = [
    path('landing/', LandingApiView.as_view()),
]