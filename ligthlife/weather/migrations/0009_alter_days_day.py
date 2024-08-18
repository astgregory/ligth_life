# Generated by Django 3.2.16 on 2024-07-07 19:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('weather', '0008_auto_20240630_1033'),
    ]

    operations = [
        migrations.AlterField(
            model_name='days',
            name='day',
            field=models.CharField(choices=[('1', 'Понедельник'), ('2', 'Вторник'), ('3', 'Среда'), ('4', 'Четверг'), ('5', 'Пятница'), ('6', 'Суббота'), ('0', 'Воскресенье')], max_length=10, unique=True),
        ),
    ]
