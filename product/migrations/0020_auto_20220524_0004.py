# Generated by Django 3.2.8 on 2022-05-23 22:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [("product", "0019_auto_20220523_2303")]

    operations = [
        migrations.AlterField(
            model_name="cartitem",
            name="id",
            field=models.AutoField(primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name="historicalcartitem",
            name="id",
            field=models.IntegerField(blank=True, db_index=True),
        ),
    ]
