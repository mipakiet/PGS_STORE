# Generated by Django 3.2.8 on 2022-05-18 19:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [("product", "0010_alter_cartitem_released_date")]

    operations = [
        migrations.AlterField(
            model_name="cartitem",
            name="released_date",
            field=models.DateField(null=True),
        )
    ]
