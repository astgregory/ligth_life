from django.contrib import admin

from .models import WeatherAlarm, Days

admin.site.register(WeatherAlarm)
admin.site.register(Days)
