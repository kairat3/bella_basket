from rest_framework import serializers
from .models import Product, Category, Favorite, Bag, Color, Size, Additional, Image


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = '__all__'

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        if instance.children.exists():
            representation['children'] = CategorySerializer(instance=instance.children.all(), many=True).data
        return representation


class AdditionalSerializer(serializers.ModelSerializer):

    class Meta:
        model = Additional
        fields = ('key', 'value', )


class IsHitSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = ('id', 'is_hit', )


class ColorSerializer(serializers.ModelSerializer):

    class Meta:
        model = Color
        fields = ('id', 'color', )


class SizeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Size
        fields = ('size', )


class ImageSerializer(serializers.ModelSerializer):

    class Meta:
        model = Image
        fields = ('title', 'image', )


class ProductSerializer(serializers.ModelSerializer):
    additional = AdditionalSerializer(many=True)
    color = ColorSerializer(many=True)
    size = SizeSerializer(many=True)
    images = ImageSerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = ('id', 'title', 'description', 'old_price', 'price', 'discount', 'additional', 'color', 'size', 'images')


class FavoriteSerializer(serializers.ModelSerializer):

    class Meta:
        model = Favorite
        fields = ('id', 'favorite', 'user', )

    def create(self, validated_data):
        request = self.context.get('request')
        user = request.user
        favorite = Favorite.objects.create(user=user, **validated_data)
        return favorite

    def to_representation(self, instance):
        representation = super(FavoriteSerializer, self).to_representation(instance)
        representation['user'] = instance.user.phone_number
        return representation


class BagSerializer(serializers.ModelSerializer):

    class Meta:
        model = Bag
        fields = ('id', 'in_bag', 'quantity', 'product')

    def create(self, validated_data):
        request = self.context.get('request')
        user = request.user
        bag = Bag.objects.create(user=user, **validated_data)
        return bag

    def to_representation(self, instance):
        representation = super(BagSerializer, self).to_representation(instance)
        representation['user'] = instance.user.phone_number
        return representation


class OrderHistorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = ('id', 'title', 'price', 'paid', )