from django.urls import path
from . import views

urlpatterns = [
    path('categories/', views.CategoryView.as_view()),
    path('categories/<slug>/', views.CategorySlugView.as_view()),
    path('favorites/', views.FavoriteListView.as_view()),
    path('bag/', views.BagListView.as_view()),
    path('bag/checkout/', views.CheckoutApiView.as_view()),
    path('ishit/', views.HitApiView.as_view()),
]
