
from .models import Car, MessageData, SentMessage, Post, FormMessage
from django.contrib import admin
from django.conf import settings
import requests
from django.http import HttpResponseRedirect
from .telegram_utils import send_telegram_message, send_select_user_telegram_message
from admin_extra_buttons.api import ExtraButtonsMixin, button
from admin_extra_buttons.utils import HttpResponseRedirectToReferrer
from django.urls import reverse
from django.utils.html import format_html



class CarAdmin(admin.ModelAdmin):
    # для отображения полей в django administration
    list_display = ('id', 'title', 'photo', 'year', 'transmission', 'engine', 'engine_type', 'body_type_mileage',
                    'price_byn', 'price_usd', 'city', 'http_link')
    # для фильтрации по полям
    list_filter = ('id', 'title', 'photo', 'year', 'transmission', 'engine', 'engine_type', 'body_type_mileage',
                   'price_byn', 'price_usd', 'city', 'http_link')
    # поиск по полям
    search_fields = ['id', 'title', 'photo', 'year', 'transmission', 'engine', 'engine_type', 'body_type_mileage',
                    'price_byn', 'price_usd', 'city', 'http_link']
    # ссылки по полям
    list_display_links = ['photo', 'http_link']

    # редактирование
    #list_editable = ['price_byn', 'price_usd']

    actions = ['send_message']

admin.site.register(Car, CarAdmin)

########################################################
class MessageDataAdmin(ExtraButtonsMixin, admin.ModelAdmin):
    # для отображения полей в django administration
    list_display = ('id', 'telegram_id', 'chat_id', 'message', 'full_date_time', 'click_on_button')
    # для фильтрации по полям
    list_filter = ('id', 'telegram_id', 'chat_id', 'message', 'full_date_time')
    # поиск по полям
    search_fields = ['id', 'telegram_id', 'chat_id', 'message', 'full_date_time']
    # ссылки по полям
    list_display_links = ['message']

    actions = ['send_message']

    def send_message(self, request, queryset):
        token = settings.TOKEN
        form_message = FormMessage.objects.first()

        if form_message:
            message = form_message.form_message

            queryset_list = list(queryset.values('chat_id'))
            queryset_repeated = [record['chat_id'] for record in queryset_list]
            querysets = list(set(queryset_repeated))

            for query in querysets:
                url = f"https://api.telegram.org/bot{token}/sendMessage?chat_id={query}&text={message}"
                requests.get(url).json()

    send_message.short_description = "Отправить сообщение выбранным пользователям"


    def click_on_button(self, message_object):
        url = reverse('create-sent-message', args=(message_object.telegram_id, message_object.message))  #?????
        return format_html('<a class="button" href="{}">Ответить</a>', url)

    click_on_button.short_description = 'Ответ на сообщение'

####
    @button(permission='demo.add_demomodel1',
            change_form=False, label='Обновить',
            html_attrs={'style': 'background-color:#808080;color:white'})
    def refresh(self, request):
        self.message_user(request, 'Обновление выполнено')
        # Optional: returns HttpResponse
        return HttpResponseRedirectToReferrer(request)
####
admin.site.register(MessageData, MessageDataAdmin)

#######################################################

class SentMessageAdmin(ExtraButtonsMixin, admin.ModelAdmin):
    change_form_template = "message_answer.html"
    # для отображения полей в django administration
    list_display = ('id', 'telegram_id', 'message', 'sentmessage_time', 'is_sent')
    # для фильтрации по полям
    list_filter = ('id', 'telegram_id', 'message', 'sentmessage_time')
    # поиск по полям
    search_fields = ['id', 'telegram_id', 'message', 'sentmessage_time']
    # ссылки по полям
    list_display_links = ['message']

    #actions = ['send_message']

    def response_change(self, request, sentmessage):
        if "message-answer" in request.POST:
            send_select_user_telegram_message(sentmessage=sentmessage)
            sentmessage.is_sent = True
            sentmessage.save()
            self.message_user(request, "Ответ на сообщение пользователя отправлено в телеграм")
            return HttpResponseRedirect(request.path_info)

        return super().response_change(request, sentmessage)

####
    @button(permission='demo.add_demomodel1',
            change_form=False, label='Обновить',
            html_attrs={'style': 'background-color:#808080;color:white'})
    def refresh(self, request):
        self.message_user(request, 'Обновление выполнено')
        # Optional: returns HttpResponse
        return HttpResponseRedirectToReferrer(request)
####
admin.site.register(SentMessage, SentMessageAdmin)
#######################################################
@admin.register(Post)
class PostAdmin(ExtraButtonsMixin, admin.ModelAdmin):
    change_form_template = "post_change_form.html"
    list_display = ('title', 'created_at', 'is_published')
    list_filter = ('title', 'created_at', 'is_published')
    # поиск по полям
    search_fields = ['title', 'created_at', 'is_published']
    # ссылки по полям
    #list_display_links = ['message']

    def response_change(self, request, post_obj):
        if "publish-telegram" in request.POST:
            send_telegram_message(post=post_obj)
            post_obj.is_published = True
            post_obj.save()
            self.message_user(request, "Опубликовано сообщение об этом посте в телеграм канале")
            return HttpResponseRedirect(request.path_info)

        return super().response_change(request, post_obj)

####
    @button(permission='demo.add_demomodel1',
            change_form=False, label='Обновить',
            html_attrs={'style': 'background-color:#808080;color:white'})
    def refresh(self, request):
        self.message_user(request, 'Обновление выполнено')
        # Optional: returns HttpResponse
        return HttpResponseRedirectToReferrer(request)
####

###########
class FormMessageAdmin(admin.ModelAdmin):
    list_display = ('form_message', 'created_time')
    list_filter = ('form_message', 'created_time')
    # поиск по полям
    search_fields = ['form_message', 'created_time']
    # ссылки по полям
    #list_display_links = ['message']

admin.site.register(FormMessage, FormMessageAdmin)