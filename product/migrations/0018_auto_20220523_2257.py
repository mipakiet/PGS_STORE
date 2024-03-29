# Generated by Django 3.2.8 on 2022-05-23 20:57

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [("product", "0017_alter_product_category")]

    operations = [
        migrations.AlterField(
            model_name="historicalproduct",
            name="price",
            field=models.DecimalField(
                decimal_places=2,
                max_digits=7,
                validators=[django.core.validators.MinValueValidator(0)],
            ),
        ),
        migrations.AlterField(
            model_name="product",
            name="price",
            field=models.DecimalField(
                decimal_places=2,
                max_digits=7,
                validators=[django.core.validators.MinValueValidator(0)],
            ),
        ),
    ]
