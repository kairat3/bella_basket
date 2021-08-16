from django.contrib import admin

from info.models import About, Image


class ImageTabularInline(admin.TabularInline):
    model = Image


class AboutUsAdmin(admin.ModelAdmin):
    inlines = [ImageTabularInline, ]
    model = About


admin.site.register(About, AboutUsAdmin)
