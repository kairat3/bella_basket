from django.urls import path
from info import views

urlpatterns = [
    path('about_us/', views.AboutUsApiView.as_view()),
]
