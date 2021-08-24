from django.db import models


class MainPage(models.Model):
    title1 = models.CharField(max_length=250)
    image1 = models.ImageField(upload_to='images/')
    title2 = models.CharField(max_length=250, blank=True)
    image2 = models.ImageField(upload_to='images/', blank=True)
    title3 = models.CharField(max_length=250, blank=True)
    image3 = models.ImageField(upload_to='images/', blank=True)

    def __str__(self):
        return self.title1, self.title2, self.title3
