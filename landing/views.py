from rest_framework import generics
from landing.models import MainPage
from landing.serializers import LandingSerializer


class LandingApiView(generics.ListAPIView):
    queryset = MainPage.objects.all()
    serializer_class = LandingSerializer