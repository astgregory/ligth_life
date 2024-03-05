from django.contrib import admin

from .models import WeatherAlarm, Message

admin.site.register(WeatherAlarm)
admin.site.register(Message)

