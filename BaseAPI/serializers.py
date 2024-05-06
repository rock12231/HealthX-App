from rest_framework import serializers
from BaseAPI.models import DataModel
# from django.contrib.auth.models import User


# Data Serializer
class DataSerializer(serializers.ModelSerializer):
    class Meta:
        model = DataModel
        fields = '__all__'
    # Override create methods
    def create(self, validated_data):
        return super().create(validated_data)
    # Override update methods
    def update(self, instance, validated_data):
        return super().update(instance, validated_data)