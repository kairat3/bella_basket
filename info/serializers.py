from rest_framework import serializers
from info.models import About, Image


class InfoImageSerializer(serializers.ModelSerializer):

    class Meta:
        model = Image
        fields = ('title', 'image', )


class AboutUsSerializer(serializers.ModelSerializer):
    images = InfoImageSerializer(many=True, read_only=True)

    class Meta:
        model = About
        fields = ('logo', 'description', 'description2', 'images', )