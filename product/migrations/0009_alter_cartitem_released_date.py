# Generated by Django 3.2.8 on 2022-05-18 19:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [("product", "0008_auto_20220518_2128")]

    operations = [
        migrations.AlterField(
            model_name="cartitem",
            name="released_date",
            field=models.DateField(blank=True),
        )
    ]
