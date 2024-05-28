from rest_framework import serializers
from .models import Apartment


class ApartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Apartment
        fields = "__all__"


class FacilityDistanceSerializer(serializers.Serializer):
    type = serializers.CharField(max_length=50)
    distance = serializers.IntegerField()
    unit = serializers.CharField(max_length=2)
