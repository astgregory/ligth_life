# Generated by Django 3.2.16 on 2024-04-07 19:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('weather', '0004_alter_days_day'),
    ]

    operations = [
        migrations.AlterField(
            model_name='days',
            name='day',
            field=models.CharField(choices=[('monday', 'Понедельник'), ('tuesday', 'Вторник'), ('wednesday', 'Среда'), ('thursday', 'Четверг'), ('friday', 'Пятница'), ('saturday', 'Суббота'), ('sunday', 'Воскресенье')], max_length=10, unique=True),
        ),
    ]
