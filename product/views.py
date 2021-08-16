from django.db.models import Q
from rest_framework import generics, permissions, viewsets, status
from rest_framework.permissions import IsAdminUser
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from django_filters import rest_framework as filters
from rest_framework.response import Response

from . import serializers
from .models import Category, Product, Bag, Favorite
from .serializers import FavoriteSerializer, BagSerializer, ProductSerializer, IsHitSerializer, \
    OrderHistorySerializer


class PermissionMixin:
    def get_permissions(self):
        if self.action == 'create':
            permissions = [IsAdminUser, ]
        elif self.action in ['update', 'partial_update', 'destroy']:
            permissions = [IsAdminUser, ]
        else:
            permissions = []
        return [perm() for perm in permissions]

    def get_serializer_context(self):
        return {'request': self.request, 'action': self.action}


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 1000


class CategoryView(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = serializers.CategorySerializer
    permission_classes = (permissions.AllowAny, )


class CategorySlugView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    lookup_field = 'slug'
    serializer_class = serializers.CategorySerializer
    permission_classes = (permissions.IsAdminUser, )


class HitApiView(generics.ListAPIView):
    queryset = Product.objects.filter(is_hit=True)
    serializer_class = IsHitSerializer


class ProductApiView(PermissionMixin, viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    pagination_class = StandardResultsSetPagination
    filters_backends = (filters.DjangoFilterBackend, )
    filterset_fields = ('title', 'price', 'category')

    def get_queryset(self):
        queryset = super().get_queryset()
        search = self.request.query_params.get('search', '')
        if search:
            queryset = queryset.filter(Q(title__icontains=search) | Q(id__icontains=search) | Q(price__icontains=search))
        return queryset

    @action(detail=True, methods=['post'])
    def favorite(self, request, pk=None):
        product = self.get_object()
        obj, created = Favorite.objects.get_or_create(user=request.user, product=product)
        if not created:
            obj.favorite = not obj.favorite
            print(obj.favorite)
            obj.save()
        added_removed = 'added' if obj.favorite else 'removed'
        return Response('Successfully {} favorite'.format(added_removed), status=status.HTTP_200_OK)

    @action(detail=True, methods=['post', 'delete'])
    def bag(self, request, pk=None):
        product = self.get_object()
        obj, created = Bag.objects.get_or_create(user=request.user, product=product)
        if obj.in_bag:
            return Response('Товар уже в корзине', status=status.HTTP_400_BAD_REQUEST)
        obj.in_bag = not obj.in_bag
        print(obj.in_bag)
        obj.save()
        return Response('Успешно добавлено в корзину', status=status.HTTP_200_OK)

    @action(detail=True, methods=['delete'])
    def bag_delete(self, request, pk=None):
        product = self.get_object()
        obj, created = Bag.objects.get_or_create(user=request.user, product=product)
        if not obj.in_bag:
            return Response('Товар уже удален', status=status.HTTP_404_NOT_FOUND)
        obj.in_bag = not obj.in_bag
        print(obj.in_bag)
        obj.save()
        return Response('Товар удален из корзины', status=status.HTTP_404_NOT_FOUND)


class FavoriteListView(generics.ListAPIView):
    queryset = Favorite.objects.all()
    serializer_class = FavoriteSerializer

    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return Favorite.objects.none()
        user = self.request.user
        queryset = Favorite.objects.filter(user=user, favorite=True)
        return queryset


class BagListView(generics.ListAPIView):
    queryset = Bag.objects.all()
    serializer_class = BagSerializer

    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return Bag.objects.none()
        user = self.request.user
        queryset = Bag.objects.filter(user=user, in_bag=True)
        return queryset


class CheckoutApiView(generics.ListAPIView):
    queryset = Product.objects.filter(paid=True)
    serializer_class = OrderHistorySerializer
