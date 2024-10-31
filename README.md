# Light Life

Light Life – это проект, который пока что включает в себя только приложение weather, позволяющее пользователям получать информацию о погоде и устанавливать оповещения о погодных условиях в различных городах.

## Пример сообщения

#### Погода для города: Ваш город

- Погода на улице: ясно
- Температура: (текущая температура) градусов по Цельсию, но ощущается как (ощущаемая температура) градусов
- Влажность воздуха: (текущая влажность воздуха) %
- Скорость ветра: (скорость в цифрах) м/с
- Облачность: (цифра) %

## Установка и настройка

### Требования

- Docker
- Docker Compose

### Установка проекта

1. Клонируйте репозиторий:

   ```bash
   git clone https://github.com/astgregory/lightlife.git
   cd lightlife

2. Запустите приложение с помощью Docker Compose:
   ```bash
   docker-compose up --build
   ```
   Это создаст и запустит контейнеры для вашего приложения, включая базу данных PostgreSQL.

3. После первого запуска, создайте суперпользователя:
   ```bash
   docker compose exec web-app python manage.py createsuperuser
4. Запустите миграции:
   ```bash
   docker compose exec web-app python manage.py migrate
   
### Конфигурация

Настройте конфигурации в файле settings.py. 

### Запуск задач Celery

Чтобы запустить задачи Celery, вы можете использовать следующую команду:
```bash
docker compose up
```
### Использование приложения Weather

#### Основные функции

- Получение прогнозов погоды для заданных городов.
- Установка оповещений о погодных условиях на электронную почту.
- Интерфейс для управления профилем пользователя и создания/удаления оповещений.

#### API
Приложение предоставляет API для взаимодействия с данными о погоде:

- Регистрация пользователя: POST /api/users/
- Управление оповещениями: GET,POST /api/weather-alarms/,
                           PUT, PATCH, DELETE /api/weather-alarms/{id}/
#### Пример добавления напоминания о погоде

Чтобы создать новое напоминание о погоде, отправьте следующий JSON в теле запроса POST /api/weather-alarms/:
```json
{
    "country": "RU",
    "city": "Moscow",
    "phone_number": "+79998887766",
    "email": "your_email@mail.com",
    "time": "00:00:00",
    "time_zone": "Europe/Moscow",
    "days": [
        {
            "day": "Вторник"
        },
        {
            "day": "Суббота"
        }
    ]
}
```
Вариация выбора полей country, time_zone и day представлены в models.py



### Примеры запросов  
```bash
# Пример регистрации
curl -X POST -d "username=example&password=pass" http://localhost:8000/api/users/

# Пример получения данных об уведомлениях о погоде
curl -u example:pass -X GET http://localhost:8000/api/weather-alarms/

# Пример добавления напоминания о погоде
curl -u example:pass -X POST -H "Content-Type: application/json" -d '{
    "country": "RU",
    "city": "Moscow",
    "phone_number": "+79998887766",
    "email": "your_email@mail.com",
    "time": "00:00:00",
    "time_zone": "Europe/Moscow",
    "days": [
        {
            "day": "Вторник"
        },
        {
            "day": "Суббота"
        }
    ]
}' http://localhost:8000/api/weather-alarms/


```
## Тестирование

Для запуска тестов используйте следующую команду:
```bash
docker-compose exec web python manage.py test
```
## Контакты

Если у вас есть какие-либо вопросы или предложения, пожалуйста, свяжитесь со мной через astgregory@bk.ru.


