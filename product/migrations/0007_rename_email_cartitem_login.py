# Generated by Django 3.2.8 on 2022-04-03 18:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [("product", "0006_cartitem_order_id")]

    operations = [
        migrations.RenameField(
            model_name="cartitem", old_name="email", new_name="login"
        )
    ]
