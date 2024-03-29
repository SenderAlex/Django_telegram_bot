# Generated by Django 5.0.2 on 2024-03-01 12:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tele_bot_app', '0010_rename_telegrammessage_message_data'),
    ]

    operations = [
        migrations.CreateModel(
            name='MessageData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('telegram_id', models.IntegerField(null=True, verbose_name='telegram_id')),
                ('chat_id', models.IntegerField(null=True, verbose_name='chat_id')),
                ('message', models.TextField(null=True, verbose_name='Сообщения')),
                ('full_date_time', models.DateTimeField(null=True, verbose_name='Дата и время получения')),
            ],
        ),
    ]
