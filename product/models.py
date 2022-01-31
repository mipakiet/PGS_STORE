from django.db import models
from django.contrib.auth.models import User
from django_jsonform.models.fields import JSONField


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
    name = models.CharField(max_length=30)
    description = models.TextField(null=True, blank=True)
    price = models.DecimalField(decimal_places=2, max_digits=7)
    image = models.ImageField(upload_to="products/")
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, null=True, blank=True
    )
    city = models.ForeignKey(City, on_delete=models.CASCADE, null=True)
    quantity = models.PositiveIntegerField(default=0)

    SPEC_SCHEMA = {
        "type": "dict",
        "keys": {
            "Model": {"type": "string"},
            "Procesor": {"type": "string"},
            "RAM": {"type": "string", "choices": ["8GB", "16GB", "24GB", "32GB"]},
            "Karta Graficzna": {"type": "string"},
            "Dysk": {"type": "string"},
            "Rozmiar": {"type": "string"},
            "Waga": {"type": "string"},
            "Uwagi": {"type": "string"},
        },
    }

    spec = JSONField(schema=SPEC_SCHEMA, null=True)

    def __str__(self):
        return self.name


class CartItem(models.Model):
    employee_name = models.CharField(max_length=50)
    address = models.CharField(max_length=50)
    company_name = models.CharField(max_length=50)
    nip = models.CharField(max_length=10, null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    price = models.DecimalField(decimal_places=2, max_digits=7)
    order_date = models.DateField(auto_now_add=True)

    bill = models.BooleanField(default=False)
    released = models.BooleanField(default=False)
    released_date = models.DateField(null=True)
