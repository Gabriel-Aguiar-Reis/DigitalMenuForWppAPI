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

    units = serializers.IntegerField(required=False, default=0)
    photos = PhotoSerializer(many=True, read_only=True)
    price = serializers.SerializerMethodField()
    post_discount_price = serializers.SerializerMethodField()

    def get_price(self, obj):
        return Util.calculate_product_price(
            obj.cost_price, obj.percentual_margin, Util.get_type_percentual_margin(obj.id)
        )

    def get_post_discount_price(self, obj, updated_units=None):
        if obj.promotion is not None:
            return Util.calculate_value_after_discount(
                self.get_price(obj),
                updated_units if updated_units is not None else obj.units,
                obj.promotion.discount_amount if obj.promotion.discount_amount is not None else 0,
                obj.promotion.percentual_discount if obj.promotion.percentual_discount is not None else 0,
                obj.promotion.unit_discount if obj.promotion.unit_discount is not None else 0,
                obj.promotion.amount_for_discount if obj.promotion.amount_for_discount is not None else 0,
                obj.promotion.unit_for_discount if obj.promotion.discount_amount is not None else 0,
            )
        else:
            return self.get_price(obj) * updated_units if updated_units is not None else obj.units


class TypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Type
        fields = '__all__'

    photos = PhotoSerializer(many=True, read_only=True)
