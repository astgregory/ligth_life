# Generated by Django 3.2.16 on 2024-06-02 19:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('weather', '0005_alter_days_day'),
    ]

    operations = [
        migrations.AddField(
            model_name='weatheralarm',
            name='email',
            field=models.EmailField(default='1@1.ru', max_length=30, unique=True, verbose_name='Адрес электронной почты'),
            preserve_default=False,
        ),
    ]