from django.contrib import admin

# Register your models here.
from django.contrib.auth.models import Group

from .models import Category, Product, Color, Bag, Additional, Size, Favorite, Image


class AdditionalTabularInline(admin.TabularInline):
    model = Additional


class AdditionalAdmin(admin.ModelAdmin):
    model = Additional


class ColorAdmin(admin.ModelAdmin):
    model = Color


class ImageTabularInline(admin.TabularInline):
    model = Image


class SizeAdmin(admin.ModelAdmin):
    model = Size


class ProductAdmin(admin.ModelAdmin):
    inlines = [AdditionalTabularInline, ImageTabularInline]
    model = Product


admin.site.register(Category)
admin.site.register(Product, ProductAdmin)
admin.site.register(Bag)
admin.site.register(Favorite)
admin.site.unregister(Group)
admin.site.register(Size)
admin.site.register(Color)
