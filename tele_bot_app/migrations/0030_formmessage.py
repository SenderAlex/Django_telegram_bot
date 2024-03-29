# Generated by Django 5.0.3 on 2024-03-16 10:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tele_bot_app', '0029_sentmessage_is_sent'),
    ]

    operations = [
        migrations.CreateModel(
            name='FormMessage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('form_message', models.TextField(null=True, verbose_name='Форма для отправки сообщения')),
                ('created_time', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name': 'Форма',
                'verbose_name_plural': 'Формы',
            },
        ),
    ]
