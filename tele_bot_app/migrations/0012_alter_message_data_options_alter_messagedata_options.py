# Generated by Django 5.0.2 on 2024-03-01 12:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tele_bot_app', '0011_messagedata'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='message_data',
            options={'verbose_name': 'Полученное сообщение', 'verbose_name_plural': 'Полученные сообщения'},
        ),
        migrations.AlterModelOptions(
            name='messagedata',
            options={'verbose_name': 'Отправленное сообщение', 'verbose_name_plural': 'Отправленные сообщения'},
        ),
    ]
