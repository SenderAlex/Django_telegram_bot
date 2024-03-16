import urllib.request
import json
from django.conf import settings
from django.template import Template, Context
from django.template.loader import render_to_string
from .models import MessageData, SentMessage


def get_html_message(post):  # альтернатива №1
    html_template = Template(
        """<a href="{{ post.url }}">{{ post.title }}</a>{{ post.content|truncatewords:30 }}"""
        """<strong>Дата создания:</strong>{{ post.created_at|date:'SHORT_DATE_FORMAT' }}""")

    return html_template.render(Context({'post': post}))


def get_html_message_from_template(post): # альтернатива №2 более безопасный
    return render_to_string('post_telegram_message.html', {
        'post': post
    })


def send_telegram_message(post):
    api_url = f'https://api.telegram.org/bot{settings.TOKEN}/sendMessage'
    records = MessageData.objects.all()
    records_list = list(records.values('chat_id'))
    chat_id_repeated = [record['chat_id'] for record in records_list]
    chat_id_list = list(set(chat_id_repeated))

    for chat_id in chat_id_list:
        input_data = json.dumps(  # преобразование словаря  в формат JSON с помощью функции json.dumps(), в результате
            # получается JSON строка
            {
                'chat_id': chat_id,  # создание словаря
                'text': get_html_message_from_template(post=post),  # создание словаря
                'parse_mode': "HTML"  # создание словаря
            }
        ).encode()  # кодирование JSON-строки в байтовый формат с использованием метода encode()

        try:
            req = urllib.request.Request(  # Создает объект req, который представляет HTTP-запрос или запрос к удаленному
                # серверу
                url=api_url,  # api_url содержит адрес сервера API, к которому обращаемся
                data=input_data,  # input_data представляет данные (сериализованные в формат JSON), которые отправляем
                # через HTTP-запрос.
                headers={'Content-Type': 'application/json'}  # application/json указывает на то, что данные, передаваемые
                # в запросе, представлены в формате JSON (чтобы сервер мог правильно интерпретировать и обработать
                # отправленные данные).
            )
            with urllib.request.urlopen(req) as response:  # выполняет отправку HTTP-запроса, созданного объектом req.
                # urlopen() инициирует запрос и возвращает объект HTTPResponse, представляющий ответ сервера.
                print(response.read().decode('utf-8'))  # выполняется чтение данных из объекта response, который содержит
                # ответ от сервера

        except Exception as e:
            print(e)


##############################################
def get_html_answer_from_template(sentmessage):
    return render_to_string('sent_telegram_answer.html', {
        'sentmessage': sentmessage
    })

#######
def send_select_user_telegram_message(sentmessage):
    api_url = f'https://api.telegram.org/bot{settings.TOKEN}/sendMessage'
    chat_id = sentmessage.telegram_id

    input_data = json.dumps(
        {
            'chat_id': chat_id,
            'text': get_html_answer_from_template(sentmessage=sentmessage),
            'parse_mode': "HTML"
        }
    ).encode()

    try:
        req = urllib.request.Request(
            url=api_url,
            data=input_data,
            headers={'Content-Type': 'application/json'}
        )
        with urllib.request.urlopen(req) as response:
            print(response.read().decode('utf-8'))

    except Exception as e:
        print(e)