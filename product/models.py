from colorfield.fields import ColorField
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser
from django.db import models
from django.db.models.signals import m2m_changed
from django.shortcuts import get_object_or_404

from account.models import CustomUser

User = get_user_model()


class Category(models.Model):
    title = models.CharField('Категория', max_length=150)
    slug = models.SlugField(unique=True, blank=True)
    image = models.ImageField('Предпросмотр', upload_to='images/', blank=True)
    parent = models.ForeignKey(
        'self', on_delete=models.CASCADE, null=True, blank=True,
        related_name='children'
    )

    def __str__(self):
        if not self.parent:
            return f"Категория: {self.title}"
        else:
            return f"{self.parent} --> {self.title}"

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Product(models.Model):
    category = models.ForeignKey(Category,verbose_name='Категория', related_name='category', on_delete=models.CASCADE)
    title = models.CharField('Название', max_length=255)
    vendor = models.CharField('Артикул', max_length=255, unique=True)
    old_price = models.DecimalField('Старая цена', max_digits=10, decimal_places=2)
    price = models.DecimalField('Новая цена', max_digits=10, decimal_places=2)
    discount = models.DecimalField('Скидка', max_digits=10, decimal_places=2)
    description = models.TextField('Описание', blank=True)
    color = models.ManyToManyField(to='product.Color', verbose_name='Цвет', related_name='product_colors')
    size = models.ManyToManyField(to='product.Size', verbose_name='Размер', related_name='размер_продукта')
    available = models.BooleanField('Наличие', default=False)
    is_hit = models.BooleanField('Хит', default=False)
    paid = models.BooleanField('Оплачено')

    def __str__(self):
        return f"{self.category}-->{self.title}"

    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'


class Image(models.Model):
    title = models.CharField(max_length=200, blank=True)
    image = models.ImageField(upload_to='images/')
    about = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')

    class Meta:
        verbose_name = 'Картинка'
        verbose_name_plural = 'Картинки'

    @staticmethod
    def generate_name():
        import random
        return "Image" + str(random.randint(1, 99999))

    def save(self, *args, **kwargs):
        self.title = self.generate_name()
        return super(Image, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.title} --> {self.about}"


class Favorite(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='favorites')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='favorites')
    favorite = models.BooleanField(default=True)

    # def __str__(self):
    #     return {self.product}

    class Meta:
        verbose_name = 'Избранное'
        verbose_name_plural = 'Избранное'


class Color(models.Model):
    title = models.CharField(verbose_name='Название цвета', max_length=256)
    color = ColorField(default='#FFFFFF')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Цвет'
        verbose_name_plural = 'Цвет'


class Additional(models.Model):
    key = models.CharField('Ключ', max_length=250, blank=True)
    value = models.CharField('Значение', max_length=250, blank=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='additional')

    def __str__(self):
        return self.key

    class Meta:
        verbose_name = 'Дополнительная информация'
        verbose_name_plural = 'Дополнительная информация'


class Size(models.Model):
    size = models.CharField('Размер', max_length=10, blank=True)

    def __str__(self):
        return self.size

    class Meta:
        verbose_name = 'Размер'
        verbose_name_plural = 'Размеры'


class CartManager(models.Manager):
    def new(self, user=None):
        user_obj = None
        if user is not None:
            if user.is_authenticated:
                user_obj = user
        return self.model.objects.create(user=user_obj)

    def get_or_new(self, request):
        user = request.user
        if isinstance(user, AnonymousUser):
            cart_obj = Cart.objects.create(user=None)
            new_obj = False
        elif Cart.objects.filter(user=user).exists():
            cart_obj = Cart.objects.get(user=user)
            new_obj = False
            if request.user.is_authenticated and not cart_obj.user:
                cart_obj.user = request.user
                cart_obj.save()
        else:
            cart_obj = Cart.objects.new(user=request.user)
            new_obj = True
            request.session['cart_id'] = cart_obj.id
        return cart_obj, new_obj


class Cart(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE,
                                related_name='cart', blank=True, null=True)
    products = models.ManyToManyField(Product, related_name='carts',
                                      blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    objects = CartManager()
    total = models.DecimalField(max_digits=20, decimal_places=2, default=0)
    subtotal = models.DecimalField(max_digits=20, decimal_places=2, default=0)

    def __str__(self):
        return f'{self.id}'


def cart_receiver(sender, instance, action, *args, **kwargs):
    if action == 'post_add' or action == 'post_remove' or action == \
            'post_clear':
        total = 0
        for x in instance.products.all():
            total += x.price
        if instance.subtotal != total:
            instance.subtotal = total
            instance.save()


m2m_changed.connect(
    cart_receiver,
    sender=Cart.products.through)
