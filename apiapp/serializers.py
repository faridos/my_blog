from rest_framework import serializers
from .models import Plant, DataPoint
from django.db import IntegrityError
from rest_framework.exceptions import ValidationError


class DataPointSerializer(serializers.ModelSerializer):
    plant = serializers.PrimaryKeyRelatedField(queryset=Plant.objects.all(),
                                               required=False)

    class Meta:
        model = DataPoint
        fields = '__all__'


class PlantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Plant
        fields = '__all__'
