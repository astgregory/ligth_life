from django.contrib import admin

from .models import WeatherAlarm, Message, Days

admin.site.register(WeatherAlarm)
admin.site.register(Days)

admin.site.register(Message)
