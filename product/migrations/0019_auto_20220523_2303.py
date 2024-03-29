# Generated by Django 3.2.8 on 2022-05-23 21:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [("product", "0018_auto_20220523_2257")]

    operations = [
        migrations.AlterField(
            model_name="cartitem", name="address", field=models.CharField(max_length=60)
        ),
        migrations.AlterField(
            model_name="cartitem",
            name="company_name",
            field=models.CharField(blank=True, max_length=30),
        ),
        migrations.AlterField(
            model_name="cartitem", name="login", field=models.CharField(max_length=25)
        ),
        migrations.AlterField(
            model_name="historicalcartitem",
            name="address",
            field=models.CharField(max_length=60),
        ),
        migrations.AlterField(
            model_name="historicalcartitem",
            name="company_name",
            field=models.CharField(blank=True, max_length=30),
        ),
        migrations.AlterField(
            model_name="historicalcartitem",
            name="login",
            field=models.CharField(max_length=25),
        ),
    ]
