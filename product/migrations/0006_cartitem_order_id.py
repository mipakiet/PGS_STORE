# Generated by Django 3.2.8 on 2022-02-16 13:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [("product", "0005_alter_product_city")]

    operations = [
        migrations.AddField(
            model_name="cartitem",
            name="order_id",
            field=models.PositiveIntegerField(default=0),
        )
    ]
