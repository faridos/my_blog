from rest_framework import serializers
from .models import Plant, DataPoint
from django.db import IntegrityError
from rest_framework.exceptions import ValidationError


class DataPointListSerializer(serializers.ModelSerializer):
    class Meta:
        model = DataPoint
        exclude = ('plant',)


class DataPointSerializer(serializers.ModelSerializer):
    plant = serializers.PrimaryKeyRelatedField(queryset=Plant.objects.all(),
                                               required=False)

    class Meta:
        model = DataPoint
        fields = '__all__'


class DataPointRawSerializer(serializers.ModelSerializer):
    solar_plant = DataPointListSerializer(source='plant_data')

    class Meta:
        model = Plant
        exclude  = ('name',)


class PlantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Plant
        fields = '__all__'
