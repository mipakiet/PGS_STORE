# Generated by Django 3.2.8 on 2022-06-28 15:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [("product", "0024_auto_20220528_2120")]

    operations = [
        migrations.AddField(
            model_name="cartitem",
            name="pgsid",
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name="historicalcartitem",
            name="pgsid",
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]
