from django.utils import timezone
from rest_framework import serializers

from .models import Campaign, Photo, Product, Type


class CampaignSerializer(serializers.ModelSerializer):
    class Meta:
        model = Campaign
        fields = '__all__'

    def validate_datetime(self, value):
        if value < timezone.now():
            raise serializers.validationError('Invalid date or time.')
        return value

class PhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Photo
        fields = '__all__'

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

    photos = PhotoSerializer(many=True, read_only=True)

class TypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Type
        fields = '__all__'

    photos = PhotoSerializer(many=True, read_only=True)
