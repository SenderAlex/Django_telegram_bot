# Generated by Django 5.0.3 on 2024-03-10 18:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tele_bot_app', '0021_typingmessage_alter_sentmessage_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='messagedata',
            name='telegram_id',
            field=models.PositiveBigIntegerField(null=True, verbose_name='telegram_id'),
        ),
    ]
