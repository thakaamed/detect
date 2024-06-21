import json
from channels.generic.websocket import AsyncWebsocketConsumer
from . models import ActiveUsers, SpecificUserLoginDiary
from User.models import *
from datetime import datetime, timedelta
from channels.db import database_sync_to_async
from django.utils import timezone

class MarkingConsumer(AsyncWebsocketConsumer):
    async def receive(self, text_data):
        # Kullanıcının etkileşimde bulunduğunda burada işlem yap
        print("RECEIVE")
        self.user_last_activity = datetime.now()
        
    async def disconnect(self, close_code):
        # WebSocket bağlantısı kapandığında burada işlem yap
        user = self.scope['user']
        print("DISCONNECTED", user,close_code)
        # try:
        #     active_user = ActiveUsers.objects.get(user=user)
        #     active_user.active_users.remove(user)
        #     active_user.active_user_count -= 1
        #     active_user.save()
        # except ActiveUsers.DoesNotExist:
        #     pass

    async def connect(self):
        await self.accept()
        user = self.scope['user']
        # self.user_last_activity = datetime.now()
        # try:
        #     active_user = ActiveUsers.objects.get_or_create()[0]
        #     active_user.active_users.add(user)
        #     active_user.active_user_count += 1
        #     active_user.save()
        # except ActiveUsers.DoesNotExist:
        #     pass
        print("CONNECTED",user)

class OnlineStatusConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()
        user = self.scope['user']
        status = True
        print("CONNECTED",user)
        await self.change_online_status(user, status)

    async def disconnect(self, close_code):
        user = self.scope['user']
        status = False
        print("DISCONNECTED", user,close_code)
        await self.change_online_status(user, status)

    @database_sync_to_async
    def change_online_status(self, user, status):
        if status:
            active_user = ActiveUsers.objects.get_or_create()[0]
            if not active_user.active_users.filter(id=user.id).exists():
                active_user.active_users.add(user)
                active_user.active_user_count += 1
                active_user.save()
                # Kullanıcının en son oturum açma girişimini al
                # last_login_attempt = SpecificUserLoginDiary.objects.filter(user=user).last()
                # # Eğer kullanıcı daha önce oturum açma girişimi yapmışsa ve son giriş denemesi 10 dakika içindeyse yeni bir obje oluştur
                # if last_login_attempt and (timezone.now() - last_login_attempt.login_date) < timedelta(minutes=2):
                #     print("Son oturum açma girişimi 30 dakika içinde yapılmış.")
                # else:
                #     specific_user_active_log = SpecificUserLoginDiary.objects.create(
                #         user=user,
                #         login_date=timezone.now()
                #     )
            else:
                print("User already connected")
        else:
            active_user = ActiveUsers.objects.get_or_create()[0]
            if active_user.active_users.filter(id=user.id).exists():
                active_user.active_users.remove(user)
                active_user.active_user_count -= 1
                active_user.save()
                # specific_user_active_log = SpecificUserLoginDiary.objects.filter().last()
                # if specific_user_active_log:
                #     specific_user_active_log.logout_date = datetime.now()
                #     specific_user_active_log.save()
            else:
                print("User already disconnected")