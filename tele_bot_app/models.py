
from django.db import models
from django.urls import reverse
from django.utils import timezone


class Car(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255, verbose_name="Наименование", null=True)
    photo = models.ImageField(blank=True, upload_to="car_photoes/%d/%m/%Y/", verbose_name="Фото", null=True)
    year = models.IntegerField(null=True, verbose_name="Год выпуска")
    transmission = models.CharField(max_length=255, verbose_name="Трансмиссия", null=True)
    engine = models.CharField(null=True, verbose_name="Объём в литрах")
    engine_type = models.CharField(max_length=255, verbose_name="Тип двигателя", null=True)
    body_type_mileage = models.CharField(max_length=255, verbose_name="Тип кузова, Пробег автомобиля", null=True)
    price_byn= models.IntegerField(verbose_name='Цена в бел. рублях', null=True)
    price_usd = models.IntegerField(verbose_name='Цена в долларах', null=True)
    city = models.CharField(max_length=255, verbose_name="Город", null=True)
    http_link = models.URLField(null=True, verbose_name="Ссылка")


    def __str__(self):
        return (f'{self.title}, {self.photo}, {self.year}, {self.transmission}, {self.engine}, {self.engine_type},'
                f'{self.body_type_mileage}, {self.price_byn}, {self.price_usd}, {self.city}, {self.http_link}')

    def get_absolute_url(self):
        return reverse('post', kwargs={'post_id': self.pk})


    class Meta:
        verbose_name = 'Автомобиль'
        verbose_name_plural = 'Автомобили'
        ordering = ['price_usd']


    def clean(self):  # чтобы id  был NOT NULL!!!
        if not self.id:
            self.id = Car.objects.last().id + 1

######################################
class MessageData(models.Model):
    id = models.AutoField(primary_key=True)
    telegram_id = models.PositiveBigIntegerField(null=True, verbose_name="telegram_id")
    chat_id = models.PositiveBigIntegerField(null=True, verbose_name="chat_id")
    message = models.TextField(null=True, verbose_name="Сообщения")
    full_date_time = models.DateTimeField(default=timezone.now, verbose_name="Дата и время получения")


    def __str__(self):
        return f'{self.telegram_id}, {self.chat_id}, {self.message}, {self.full_date_time}'

    # def get_absolute_url(self):
    #     return reverse('post', kwargs={'post_id': self.pk})


    class Meta:
        verbose_name = 'Полученное сообщение'
        verbose_name_plural = 'Полученные сообщения'
        ordering = ('full_date_time',)


    def clean(self):  # чтобы id  был NOT NULL!!!
        if not self.id:
            self.id = MessageData.objects.last().id + 1

#######################################
class SentMessage(models.Model):
    id = models.AutoField(primary_key=True)
    telegram_id = models.PositiveBigIntegerField(null=True, verbose_name="telegram_id")
    message = models.TextField(null=True, verbose_name="Сообщения")
    sentmessage_time = models.DateTimeField(default=timezone.now, verbose_name="Дата и время отправления")
    is_sent = models.BooleanField(default=False, verbose_name="Отметка об отправлении")



    def __str__(self):
        return f'{self.telegram_id}, {self.message}, {self.sentmessage_time}'

    # def get_absolute_url(self):
    #     return reverse('post', kwargs={'post_id': self.pk})


    class Meta:
        verbose_name = 'Отправленное сообщение'
        verbose_name_plural = 'Отправленные сообщения'
        ordering = ('sentmessage_time',)


    def clean(self):  # чтобы id  был NOT NULL!!!
        if not self.id:
            self.id = SentMessage.objects.last().id + 1

#######################################
class Post(models.Model):
    title = models.CharField(max_length=255)
    url = models.CharField(max_length=255)
    content = models.TextField()
    created_at = models.DateTimeField(default=timezone.now, verbose_name="Дата и время отправления")
    is_published = models.BooleanField(default=False, verbose_name="Отметка об отправлении")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'
        ordering = ('created_at',)

##########

class FormMessage(models.Model):
    form_message = models.TextField(null=True, verbose_name="Форма для отправки сообщения")
    created_time = models.DateTimeField(auto_now_add=True, verbose_name="Время создания сообщения")

    def __str__(self):
        return f'{self.form_message}, {self.created_time}'

    class Meta:
        verbose_name = 'Форма'
        verbose_name_plural = 'Формы'
