
from .serializers import CarSerializer, MessageDataSerializer, SentMessageSerializer
from rest_framework import viewsets, filters, generics
from .permissions import AllForAdminOtherReadOnly
from rest_framework.pagination import PageNumberPagination
from .models import Car, MessageData, SentMessage, Post
from django.http import HttpResponse, HttpResponseRedirect
from .telegram_utils import send_telegram_message, send_select_user_telegram_message
from django.urls import reverse



def send_post_to_telegram_view(request):
    post = Post.objects.first()
    send_telegram_message(post=post)
    return HttpResponse("Send telegram message")


def send_message_to_telegram_view(request):
    sentmessage = SentMessage.objects.first()
    send_select_user_telegram_message(sentmessage=sentmessage)
    return HttpResponse("Send telegram answer")


def create_sent_message(request, telegram_id, message):
    # создание объекта класса SentMessage
    sent_message = SentMessage.objects.create(telegram_id=telegram_id, message=message)
    # перенаправление на страницу где вводятся данные модели SentMessage
    url = reverse('admin:tele_bot_app_sentmessage_change', args=[sent_message.id])
    return HttpResponseRedirect(url)

#################################################################################################

class CarAPIListPagination(PageNumberPagination):  # определенная пагинация
    page_size = 3
    page_size_query_param = 'page_size'
    max_page_size = 100

class CarViewSet(viewsets.ModelViewSet):
    queryset = Car.objects.all()
    serializer_class = CarSerializer
    permission_classes = (AllForAdminOtherReadOnly, )  # IsAuthenticatedOrReadOnly -- права доступа только по чтению
    #filter_backends = [filters.SearchFilter]  # фильтрация данных по поиску
    filter_backends = [filters.OrderingFilter]  # фильтрация данных по сортировке в виде http://127.0.0.1:8000/api/player/?ordering=price_usd

    # поиск осуществляется в виде http://127.0.0.1:8000/api/player/?search=2020
    search_fields = ['title', 'photo', 'year', 'transmission', 'engine', 'engine_type', 'body_type_mileage',
                    'price_byn', 'price_usd', 'city', 'http_link']

    pagination_class = CarAPIListPagination  # определенная пагинация


class CarCreate(generics.ListCreateAPIView):
    queryset = Car.objects.all()
    serializer_class = CarSerializer


class CarRetrieveUpdateDelete(generics.RetrieveUpdateDestroyAPIView):
    queryset = Car.objects.all()
    serializer_class = CarSerializer

#########################################################

class MessageDataAPIListPagination(PageNumberPagination):  # определенная пагинация
    page_size = 3
    page_size_query_param = 'page_size'
    max_page_size = 100


class MessageDataViewSet(viewsets.ModelViewSet):
    queryset = MessageData.objects.all()
    serializer_class = MessageDataSerializer
    permission_classes = (AllForAdminOtherReadOnly, )  # IsAuthenticatedOrReadOnly -- права доступа только по чтению
    #filter_backends = [filters.SearchFilter]  # фильтрация данных по поиску
    filter_backends = [filters.OrderingFilter]  # фильтрация данных по сортировке в виде http://127.0.0.1:8000/api/player/?ordering=price_usd

    # поиск осуществляется в виде http://127.0.0.1:8000/api/player/?search=2020
    search_fields = ['telegram_id', 'chat_id', 'message']

    pagination_class = MessageDataAPIListPagination  # определенная пагинация


class MessageDataCreate(generics.ListCreateAPIView):
    queryset = MessageData.objects.all()
    serializer_class = MessageDataSerializer


class MessageDataRetrieveUpdateDelete(generics.RetrieveUpdateDestroyAPIView):
    queryset = MessageData.objects.all()
    serializer_class = MessageDataSerializer

###########################################################################

class SentMessageAPIListPagination(PageNumberPagination):  # определенная пагинация
    page_size = 3
    page_size_query_param = 'page_size'
    max_page_size = 100


class SentMessageViewSet(viewsets.ModelViewSet):
    queryset = SentMessage.objects.all()
    serializer_class = SentMessageSerializer
    permission_classes = (AllForAdminOtherReadOnly, )  # IsAuthenticatedOrReadOnly -- права доступа только по чтению
    #filter_backends = [filters.SearchFilter]  # фильтрация данных по поиску
    filter_backends = [filters.OrderingFilter]  # фильтрация данных по сортировке в виде http://127.0.0.1:8000/api/player/?ordering=price_usd

    # поиск осуществляется в виде http://127.0.0.1:8000/api/player/?search=2020
    search_fields = ['telegram_id', 'message']

    pagination_class = SentMessageAPIListPagination  # определенная пагинация


class SentMessageCreate(generics.ListCreateAPIView):
    queryset = SentMessage.objects.all()
    serializer_class = SentMessageSerializer


class SentMessageRetrieveUpdateDelete(generics.RetrieveUpdateDestroyAPIView):
    queryset = SentMessage.objects.all()
    serializer_class = SentMessageSerializer

