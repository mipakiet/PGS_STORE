# Generated by Django 3.2.8 on 2022-05-21 13:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [("product", "0014_auto_20220521_1501")]

    operations = [
        migrations.AlterField(
            model_name="cartitem",
            name="company_name",
            field=models.CharField(blank=True, max_length=50),
        ),
        migrations.AlterField(
            model_name="cartitem",
            name="nip",
            field=models.CharField(blank=True, max_length=10),
        ),
        migrations.AlterField(
            model_name="historicalcartitem",
            name="company_name",
            field=models.CharField(blank=True, max_length=50),
        ),
        migrations.AlterField(
            model_name="historicalcartitem",
            name="nip",
            field=models.CharField(blank=True, max_length=10),
        ),
    ]
