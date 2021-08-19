from django.urls import path
from . import views
from .views import CartAddAPIView

urlpatterns = [
    path('categories/', views.CategoryView.as_view()),
    path('categories/<slug>/', views.CategorySlugView.as_view()),
    path('favorites/', views.FavoriteListView.as_view()),
    path('ishit/', views.HitApiView.as_view()),
    path('cart/', CartAddAPIView.as_view())
]
