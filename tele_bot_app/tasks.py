
from celery import shared_task
from django.conf import settings
import requests
from .models import MessageData


@shared_task
def send_scheduled_message_task():
    token = settings.TOKEN
    message = "Ваше автоматически отправленное сообщение"

    queryset = MessageData.objects.all()  # нужно вставить требуемую модель
    for obj in queryset:
        url = f"https://api.telegram.org/bot{token}/sendMessage?chat_id={obj.chat_id}&text={message}"
        requests.get(url).json()


# необходимо запустить следующие команды
# celery -A your_project_name worker --beat --scheduler django --loglevel=info