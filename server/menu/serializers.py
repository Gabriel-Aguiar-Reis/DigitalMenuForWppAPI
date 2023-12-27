from django.utils import timezone
from rest_framework import serializers

from .models import Campaign, Photo, Product, Type
from .utils import Util


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
    final_price = serializers.SerializerMethodField()

    def get_final_price(self, obj):
        return Util.calculate_product_price(
            obj.cost_price, obj.percentual_margin, obj.type.percentual_margin
        )
    units_purchased = serializers.SerializerMethodField()
    
    def get_units_purchased(self, obj):
        self.units_purchased = 10
        return self.units_purchased
    
    product_total_price = serializers.SerializerMethodField()

    def get_product_total_price(self, obj): 
        return Util.calculate_value_after_discount(
            self.get_final_price(obj),
            self.get_units_purchased(obj),
            obj.promotion.discount_amount,
            obj.promotion.percentual_discount,
            obj.promotion.unit_discount,
            obj.promotion.amount_for_discount,
            obj.promotion.unit_for_discount,
        )


class TypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Type
        fields = '__all__'

    photos = PhotoSerializer(many=True, read_only=True)
