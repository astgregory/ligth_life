# Generated by Django 3.2.16 on 2024-04-06 19:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('weather', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='weatheralarm',
            name='days',
        ),
        migrations.AddField(
            model_name='weatheralarm',
            name='days',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='weather.days', verbose_name='Дни уведомлений'),
        ),
    ]
