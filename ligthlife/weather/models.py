import requests

from django.core.validators import RegexValidator
from django.db import models
from django.contrib.auth.models import User


class Days(models.Model):
    DAYS_OF_WEEK_CHOICES = (
        ('monday', 'Понедельник'),
        ('tuesday', 'Вторник'),
        ('wednesday', 'Среда'),
        ('thursday', 'Четверг'),
        ('friday', 'Пятница'),
        ('saturday', 'Суббота'),
        ('sunday', 'Воскресенье'),

    )
    day = models.CharField(max_length=10, choices=DAYS_OF_WEEK_CHOICES, unique=True)

    def __str__(self):
        return self.day


class WeatherAlarm(models.Model):
    COUNTRY_CHOICES = (
        ('AF', 'Afghanistan'),
        ('AL', 'Albania'),
        ('DZ', 'Algeria'),
        ('AR', 'Argentina'),
        ('AU', 'Australia'),
        ('AT', 'Austria'),
        ('BD', 'Bangladesh'),
        ('BE', 'Belgium'),
        ('BR', 'Brazil'),
        ('BG', 'Bulgaria'),
        ('CA', 'Canada'),
        ('CN', 'China'),
        ('CO', 'Colombia'),
        ('HR', 'Croatia'),
        ('CZ', 'Czech Republic'),
        ('DK', 'Denmark'),
        ('EG', 'Egypt'),
        ('FI', 'Finland'),
        ('FR', 'France'),
        ('DE', 'Germany'),
        ('GR', 'Greece'),
        ('HU', 'Hungary'),
        ('IN', 'India'),
        ('ID', 'Indonesia'),
        ('IR', 'Iran'),
        ('IT', 'Italy'),
        ('JP', 'Japan'),
        ('KZ', 'Kazakhstan'),
        ('KE', 'Kenya'),
        ('KR', 'South Korea'),
        ('KW', 'Kuwait'),
        ('MY', 'Malaysia'),
        ('MX', 'Mexico'),
        ('NL', 'Netherlands'),
        ('NZ', 'New Zealand'),
        ('NG', 'Nigeria'),
        ('NO', 'Norway'),
        ('PK', 'Pakistan'),
        ('PE', 'Peru'),
        ('PH', 'Philippines'),
        ('PL', 'Poland'),
        ('PT', 'Portugal'),
        ('RO', 'Romania'),
        ('RU', 'Russia'),
        ('SA', 'Saudi Arabia'),
        ('RS', 'Serbia'),
        ('SG', 'Singapore'),
        ('ZA', 'South Africa'),
        ('ES', 'Spain'),
        ('SE', 'Sweden'),
        ('CH', 'Switzerland'),
        ('TH', 'Thailand'),
        ('TR', 'Turkey'),
        ('UA', 'Ukraine'),
        ('AE', 'United Arab Emirates'),
        ('GB', 'United Kingdom'),
        ('US', 'United States'),
        ('VN', 'Vietnam'),
    )

    phone_regex = RegexValidator(
        regex=r'^\+?\d{11}$',
        message="Номер телефона должен быть в формате: '+79998887766'. Требуется длина номера - 11 цифр."
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    country = models.CharField(max_length=2, choices=COUNTRY_CHOICES, verbose_name='Страна')
    city = models.CharField(max_length=100, verbose_name='Город')
    phone_number = models.CharField(
        validators=[phone_regex],
        max_length=13,
        unique=True,
        null=True,
        verbose_name='Номер телефона'
    )

    days = models.ManyToManyField(Days, verbose_name='Дни уведомлений', null=True)

    time = models.TimeField(verbose_name='Время уведомлений', null=True)
    lat = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
    lon = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)

    def __str__(self):
        return f"{self.user.username.title()}'s alarms"

    def save(self, *args, **kwargs):
        api_key = 'bddaad7f3cc6c78be3d257780671d344'
        url = f"http://api.openweathermap.org/geo/1.0/direct?q={self.city},{self.country}&appid={api_key}"
        response = requests.get(url)

        if response.status_code == 200:
            data = response.json()
            if data:
                self.lat = data[0]['lat']
                self.lon = data[0]['lon']

        super(WeatherAlarm, self).save(*args, **kwargs)


class Message(models.Model):
    weather_alarm = models.ForeignKey(WeatherAlarm, on_delete=models.CASCADE)
    text = models.TextField()
    status = models.CharField(max_length=50)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.text
