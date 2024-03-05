from django.db import models
from django.contrib.auth.models import User

class WeatherAlarm(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    country = models.CharField(max_length=100)
    city = models.CharField(max_length=100)

    def __str__(self):
        return self.user.username

class Message(models.Model):
    weather_alarm = models.ForeignKey(WeatherAlarm, on_delete=models.CASCADE)
    text = models.TextField()
    status = models.CharField(max_length=50)  # например, 'отправлено', 'не отправлено'
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.text