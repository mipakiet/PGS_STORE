# Generated by Django 3.2.8 on 2021-10-08 14:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [("Product", "0007_alter_product_image")]

    operations = [
        migrations.CreateModel(
            name="Computer",
            fields=[
                (
                    "product_ptr",
                    models.OneToOneField(
                        auto_created=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        parent_link=True,
                        primary_key=True,
                        serialize=False,
                        to="Product.product",
                    ),
                ),
                ("Ram", models.DecimalField(decimal_places=0, max_digits=6)),
            ],
            bases=("Product.product",),
        )
    ]
