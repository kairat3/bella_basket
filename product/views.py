from django.db.models import Q
from rest_framework import generics, permissions, viewsets, status
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAdminUser
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from django_filters import rest_framework as filters
from rest_framework.response import Response
from rest_framework.views import APIView

from . import serializers
from .models import Category, Product, Favorite, Cart
from account.permissions import IsOwnerOrReadOnly
from .serializers import FavoriteSerializer, ProductSerializer, IsHitSerializer, CartSerializer, AddToCartSerializer


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
    permission_classes = (IsOwnerOrReadOnly, )


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


class FavoriteListView(generics.ListAPIView):
    queryset = Favorite.objects.all()
    serializer_class = FavoriteSerializer

    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return Favorite.objects.none()
        user = self.request.user
        queryset = Favorite.objects.filter(user=user, favorite=True)
        return queryset


class CartAddAPIView(APIView):
    def get(self, request):
        cart_obj, new_obj = Cart.objects.get_or_new(request)
        serializer = CartSerializer(cart_obj)
        return Response(serializer.data)

    def post(self, request):
        cart = Cart.objects.get_or_new(request)[0]
        serializer_context = {'request': request}
        serializer = AddToCartSerializer(data=request.data,
                                         context=serializer_context)
        serializer.is_valid(raise_exception=True)
        product = get_object_or_404(Product,
                                    pk=serializer.validated_data.get('id'))
        if product in cart.products.all():
            cart.products.remove(product)
        else:
            cart.products.add(product)
        return Response(status=status.HTTP_201_CREATED)

    def get_object(self):
        return self.request.user
