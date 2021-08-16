from rest_framework import generics
from info import serializers
from info.models import About, Image


class AboutUsApiView(generics.ListAPIView):
    queryset = About.objects.all()
    serializer_class = serializers.AboutUsSerializer
