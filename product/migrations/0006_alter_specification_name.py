# Generated by Django 3.2.8 on 2022-02-07 17:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [("product", "0005_remove_product_items")]

    operations = [
        migrations.AlterField(
            model_name="specification",
            name="name",
            field=models.CharField(max_length=18, unique=True),
        )
    ]