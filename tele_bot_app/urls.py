
from django.urls import path, include
from rest_framework import routers
from .views import CarViewSet, MessageDataViewSet, SentMessageViewSet
from .views import (send_post_to_telegram_view, send_message_to_telegram_view, create_sent_message)#sent_message_view, sent_message,


router = routers.DefaultRouter()
router.register('Car', CarViewSet)

router2 = routers.DefaultRouter()
router2.register('MessageData', MessageDataViewSet)

router3 = routers.DefaultRouter()
router3.register('SentMessage', SentMessageViewSet)


urlpatterns = [
    path('', include(router.urls)),
    path('', include(router2.urls)),
    path('', include(router3.urls)),
    path('send_telegram/', send_post_to_telegram_view),
    path('send_answer/', send_message_to_telegram_view),
    path('create-sent-message/<int:telegram_id>/<str:message>/', create_sent_message, name='create-sent-message'),
    path('auth/', include('rest_framework.urls')),  # осуществляет log out в API???????
]
