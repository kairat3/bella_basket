from rest_framework import serializers
from landing.models import MainPage


class LandingSerializer(serializers.ModelSerializer):

    class Meta:
        model = MainPage
        fields = '__all__'
