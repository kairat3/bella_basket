from rest_framework import serializers

from account.serializers import ProfileSerializer, UserSerializer
from .models import Product, Category, Favorite, Color, Size, Additional, Image


class AdditionalSerializer(serializers.ModelSerializer):

    class Meta:
        model = Additional
        fields = ('key', 'value', )



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


class IsHitSerializer(serializers.ModelSerializer):
    images = ImageSerializer(many=True, read_only=True)
    color = ColorSerializer(many=True)
    size = SizeSerializer(many=True)

    class Meta:
        model = Product
        fields = (
        'id', 'is_hit', 'title', 'description', 'old_price', 'price', 'discount', 'additional', 'color', 'size',
        'images', 'category')


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ('id', 'title', 'slug',)

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation2 = super(ProductSerializer)
        print(representation2)
        if instance.children.exists():
            representation['children'] = CategorySerializer(instance=instance.children.all(), many=True).data
        return representation


class ProductSerializer(serializers.ModelSerializer):
    additional = AdditionalSerializer(many=True)
    color = ColorSerializer(many=True)
    size = SizeSerializer(many=True)
    images = ImageSerializer(many=True, read_only=True)
    category = CategorySerializer()

    class Meta:
        model = Product
        fields = ('id', 'title', 'description', 'old_price', 'price', 'discount', 'additional', 'color', 'size', 'images', 'category', 'is_hit')


class FavoriteSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)

    class Meta:
        model = Favorite
        fields = ('id', 'favorite', 'user', 'product')

    def create(self, validated_data):
        request = self.context.get('request')
        user = request.user
        favorite = Favorite.objects.create(user=user, **validated_data)
        return favorite

    def to_representation(self, instance):
        representation = super(FavoriteSerializer, self).to_representation(instance)
        representation['user'] = instance.user.phone_number
        return representation


class CartSerializer(serializers.Serializer):
    user = ProfileSerializer()
    products = ProductSerializer(many=True)
    created_at = serializers.DateTimeField()


class AddToCartSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()

    class Meta:
        model = Product
        fields = ['id']
