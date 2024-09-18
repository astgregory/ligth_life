from rest_framework import viewsets
from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import WeatherAlarm, Days
from .serializers import UserSerializer, WeatherAlarmSerializer, DaysSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class DaysViewSet(viewsets.ModelViewSet):
    queryset = Days.objects.all()
    serializer_class = DaysSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'post': serializer.data})

    def put(self, request, *args, **kwargs):
        pk = kwargs.get('pk', None)
        if not pk:
            return Response({'error': 'Method PUT not allowed'})
        try:
            instance = Days.objects.get(pk=pk)
        except:
            return Response({'error': "Object does not exists"})
        serializer = self.serializer_class(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'put': serializer.data})



class WeatherAlarmViewSet(viewsets.ModelViewSet):
    queryset = WeatherAlarm.objects.all()
    serializer_class = WeatherAlarmSerializer

    def perform_create(self, serializer):
        weather_alarm = serializer.save()
        days_data = self.request.data.get('days', [])
        for day_data in days_data:
            day = Days.objects.create(day=day_data['day'])
            weather_alarm.days.add(day)

