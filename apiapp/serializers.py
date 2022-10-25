from rest_framework import serializers
from .models import Plant, DataPoint
from django.db import IntegrityError
from rest_framework.exceptions import ValidationError


# class DataPointSerializer(serializers.ModelSerializer):
#     plant = serializers.PrimaryKeyRelatedField(queryset=Plant.objects.all(),
#                                                required=False)
#
#     class Meta:
#         model = DataPoint
#         fields = '__all__'
#
#     def create(self, validated_data):
#         instance = DataPoint(**validated_data)
#         instance.save()
#         return instance

# class BulkCreateListSerializer(serializers.ListSerializer):
#     def create(self, validated_data):
#         result = [self.child.create(attrs) for attrs in validated_data]
#
#         try:
#             self.child.Meta.model.objects.bulk_create(result)
#         except IntegrityError as e:
#             raise ValidationError(e)
#
#         return result

#
# class ModelObjectidField(serializers.Field):
#     """
#         We use this when we are doing bulk create/update. Since multiple instances share
#         many of the same fk objects we validate and query the objects first, then modify the request data
#         with the fk objects. This allows us to pass the objects in to be validated.
#     """
#
#     def to_representation(self, value):
#         return value.id
#
#     def to_internal_value(self, data):
#         return data


class DataPointSerializer(serializers.ModelSerializer):
    # plant = ModelObjectidField()

    # def create(self, validated_data):
    #     instance = DataPoint(**validated_data)
    #
    #     if isinstance(self._kwargs["data"], dict):
    #         instance.save()
    #
    #     return instance

    class Meta:
        model = DataPoint
        fields = '__all__'


class PlantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Plant
        fields = '__all__'
