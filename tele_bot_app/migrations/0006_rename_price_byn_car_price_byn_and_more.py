# Generated by Django 5.0.2 on 2024-02-27 06:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tele_bot_app', '0005_alter_car_price_usd'),
    ]

    operations = [
        migrations.RenameField(
            model_name='car',
            old_name='price_BYN',
            new_name='price_byn',
        ),
        migrations.RenameField(
            model_name='car',
            old_name='price_USD',
            new_name='price_usd',
        ),
    ]
