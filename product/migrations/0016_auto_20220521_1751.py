# Generated by Django 3.2.8 on 2022-05-21 15:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [("product", "0015_auto_20220521_1504")]

    operations = [
        migrations.RenameField(
            model_name="cartitem", old_name="bill", new_name="billed"
        ),
        migrations.RenameField(
            model_name="historicalcartitem", old_name="bill", new_name="billed"
        ),
    ]
