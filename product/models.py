from django.db import models
from django.contrib.auth.models import User


class Producer(models.Model):
    name = models.CharField(max_length=25)

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=25)
    image = models.ImageField(upload_to="images/categories/", null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"


class City(models.Model):
    name = models.CharField(max_length=10)
    shortcut = models.CharField(max_length=3, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Cities"


class Product(models.Model):

    title = models.CharField(max_length=25)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to="images/", null=True, blank=True)
    producer = models.ForeignKey(
        Producer, on_delete=models.CASCADE, null=True, blank=True
    )
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, null=True, blank=True
    )
    city = models.ForeignKey(City, on_delete=models.CASCADE, null=True)
    quantity = models.DecimalField(max_digits=1000, decimal_places=0, default=0)

    def __str__(self):
        return self.title


class Computer(Product):
    ram = models.DecimalField(max_digits=6, decimal_places=0)


class CartItem(models.Model):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, null=True, blank=True
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    quantity = models.DecimalField(max_digits=1000, decimal_places=0, default=0)
