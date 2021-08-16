from colorfield.fields import ColorField
from django.db import models
from account.models import CustomUser


class Category(models.Model):
    name = models.CharField('Категория', max_length=150)
    slug = models.SlugField(unique=True, blank=True)
    image = models.ImageField('Предпросмотр', upload_to='images/', blank=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')

    def __str__(self):
        if not self.parent:
            return f"Категория: {self.name}"
        else:
            return f"{self.parent} --> {self.name}"

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


class Bag(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='bag')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='bag')
    quantity = models.PositiveSmallIntegerField(default=1)
    in_bag = models.BooleanField(default=True)

    def __str__(self):
        return {self.user}

    class Meta:
        verbose_name = 'Корзина'
        verbose_name_plural = 'Корзина'


class Favorite(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='favorites')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='favorites')
    favorite = models.BooleanField(default=True)

    def __str__(self):
        return {self.user}

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
