# Generated by Django 3.2.8 on 2021-10-29 17:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Product', '0012_city_shortcut'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='cuantity',
            field=models.DecimalField(decimal_places=0, default=0, max_digits=100),
        ),
    ]