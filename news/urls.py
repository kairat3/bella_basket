from django.urls import path

from news import views

urlpatterns = [
    path('news/', views.NewsListApiView.as_view()),
    path('news/<int:pk>/', views.NewsRetrieveApiView.as_view()),
]
