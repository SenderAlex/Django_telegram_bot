# Generated by Django 5.0.3 on 2024-03-10 16:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tele_bot_app', '0019_remove_sentmessage_messagedata'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sentmessage',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]