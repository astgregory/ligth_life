import requests

from django.core.validators import RegexValidator
from django.db import models
from django.contrib.auth.models import User


class Days(models.Model):
    DAYS_OF_WEEK_CHOICES = (
        ('Понедельник', 'Понедельник'),
        ('Вторник', 'Вторник'),
        ('Среда', 'Среда'),
        ('Четверг', 'Четверг'),
        ('Пятница', 'Пятница'),
        ('Суббота', 'Суббота'),
        ('Воскресенье', 'Воскресенье'),
    )
    day = models.CharField(max_length=11, choices=DAYS_OF_WEEK_CHOICES, unique=True)

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

    ZONE_CHOICES = (
        ('Europe/Astrakhan', 'Астрахань'),
        ('Europe/Volgograd', 'Волгоград'),
        ('Europe/Zaporozhye', 'Запорожье'),
        ('Europe/Kaliningrad', 'Калининград'),
        ('Europe/Moscow', 'Москва'),
        ('Europe/Samara', 'Самара'),
        ('Europe/Saratov', 'Саратов'),
        ('Europe/Simferopol', 'Симферополь'),
        ('Europe/Uzhgorod', 'Ужгород'),
        ('Europe/Ulyanovsk', 'Ульяновск'),
        ('UTC', 'UTC'),
    )

    phone_regex = RegexValidator(
        regex=r'^\+?\d{11}$',
        message="Номер телефона должен быть в формате: '+79998887766'. Требуется длина номера - 11 цифр."
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='Пользователь', unique=False)
    country = models.CharField(max_length=2, choices=COUNTRY_CHOICES, verbose_name='Страна')
    city = models.CharField(max_length=100, verbose_name='Город')
    phone_number = models.CharField(
        validators=[phone_regex],
        max_length=13,
        unique=True,
        null=True,
        verbose_name='Номер телефона'
    )
    email = models.EmailField(max_length=30, unique=True, verbose_name='Адрес электронной почты')
    days = models.ManyToManyField(Days, verbose_name='Дни уведомлений', null=True)

    time = models.TimeField(verbose_name='Время уведомлений', null=True)
    lat = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
    lon = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
    time_zone = models.CharField(max_length=100, choices=ZONE_CHOICES, verbose_name='Часовой пояс')

    def __str__(self):
        return f"{self.user.username.title()}'s alarms"

    def save(self, *args, flag=True, **kwargs):

        super(WeatherAlarm, self).save(*args, **kwargs)
        if flag:
            from weather.tasks import set_latitude_and_longitude
            set_latitude_and_longitude.delay(self.id)

    def get_weather_data(self):
        api_key = 'e796fce1a1eec7055ae4f1a3f2637930'
        url = f'https://ru.api.openweathermap.org/data/2.5/weather?lat={self.lat}&lon={self.lon}&appid={api_key}&lang={self.country}&units=metric'
        response = requests.get(url)

        if response.status_code == 200:
            weather_data = response.json()
            if 'weather' in weather_data:
                return (f'Погода на улице: {weather_data["weather"][0]["description"]}\n'
                        f'Температура: {weather_data["main"]["temp"]} градусов по Цельсию, но ощущается как {weather_data["main"]["feels_like"]} градусов\n'
                        f'Влажность воздуха: {weather_data["main"]["humidity"]} %\n'
                        f'Скорость ветра: {weather_data["wind"]["speed"]} м/с\n'
                        f'Облачность: {weather_data["clouds"]["all"]} %\n')
            else:
                return 'Ошибка получения данных о погоде: API вернуло пустой список weather'
        else:
            return f'Ошибка получения данных о погоде: {response.status_code}'
