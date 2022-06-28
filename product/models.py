from django.db import models
from django.contrib.auth.models import User
from django_jsonform.models.fields import JSONField
import os
from uuid import uuid4
from django.utils.translation import gettext_lazy as _
from simple_history.models import HistoricalRecords
from django.core.validators import MinValueValidator


class Category(models.Model):
    name = models.CharField(max_length=25)
    image = models.ImageField(upload_to="images/categories/", null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"


class Specification(models.Model):
    name = models.CharField(max_length=18, unique=True)

    def __str__(self):
        return self.name


def get_schema():
    SPEC_SCHEMA = {"type": "dict", "keys": {}}
    spec = Specification.objects.all()
    for item in spec:
        SPEC_SCHEMA["keys"][item.name] = {"type": "string"}

    return SPEC_SCHEMA


def path_and_rename(instance, filename):
    upload_to = "products"
    print(upload_to)
    ext = filename.split(".")[-1]
    # get filename
    if instance.pk:
        filename = "{}.{}".format(instance.pk, ext)
    else:
        # set filename as random string
        filename = "{}.{}".format(uuid4().hex, ext)
    # return the whole path to the file
    return os.path.join(upload_to, filename)


class Product(models.Model):
    class City(models.TextChoices):
        Wroclaw = "WRO", _("Wrocław")
        Rzeszow = "RZE", _("Rzeszów")
        Gdansk = "GDA", _("Gdańsk")

    name = models.CharField(max_length=30)
    description = models.TextField(null=True, blank=True)
    price = models.DecimalField(
        decimal_places=2, max_digits=7, validators=[MinValueValidator(0)]
    )
    image = models.ImageField(upload_to=path_and_rename)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    city = models.CharField(max_length=3, choices=City.choices, default=City.Wroclaw)
    quantity = models.PositiveIntegerField(default=0)

    spec = JSONField(schema=get_schema, null=True)
    history = HistoricalRecords()

    def __str__(self):
        return self.name


class CartItem(models.Model):
    order_id = models.PositiveIntegerField(default=0)
    employee_name = models.CharField(max_length=50)
    login = models.CharField(max_length=25)
    address = models.CharField(max_length=60)
    company_name = models.CharField(max_length=30, blank=True)
    nip = models.CharField(max_length=10, blank=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1, validators=[MinValueValidator(1)])
    price = models.DecimalField(decimal_places=2, max_digits=7)
    order_date = models.DateField(auto_now_add=True)
    pgsid = models.CharField(max_length=50, blank=True, null=True)

    billed = models.BooleanField(default=False)
    released = models.BooleanField(default=False)
    released_date = models.DateField(null=True, blank=True)
    history = HistoricalRecords()

    def __str__(self):
        return "Order number: " + str(self.id)
