from .models import Car, MessageData
from rest_framework import serializers


class CarSerializer(serializers.ModelSerializer):

    class Meta:
        model = Car
        fields = ('id', 'title', 'photo', 'year', 'transmission', 'engine', 'engine_type', 'body_type_mileage',
                    'price_byn', 'price_usd', 'city', 'http_link')
        # можно вместо всех этих полей '__all__'
        extra_kwargs = {'id': {'read_only': False}}

######################################################
class MessageDataSerializer(serializers.ModelSerializer):

    class Meta:
        model = MessageData
        fields = ('id', 'telegram_id', 'chat_id', 'message', 'full_date_time')
        # можно вместо всех этих полей '__all__'
        extra_kwargs = {'id': {'read_only': False}}

######################################################

class SentMessageSerializer(serializers.ModelSerializer):

    class Meta:
        model = MessageData
        fields = ('id', 'telegram_id',  'message', 'sentmessage_time', 'is_sent')
        # можно вместо всех этих полей '__all__'
        extra_kwargs = {'id': {'read_only': False}}