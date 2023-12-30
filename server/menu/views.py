from rest_framework import generics, status
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Campaign, Photo, Product, Type
from .serializers import (
    CampaignSerializer,
    PhotoSerializer,
    ProductSerializer,
    TypeSerializer,
)


class UpdateCart(APIView):
    def patch(self, request, pk, units_purchased, *args, **kwargs):
        product_uuid = pk

        session_key = request.session.session_key
        if not session_key:
            request.session.create()

        cart = request.session.get('cart', {'products': []})
        products = cart.get('products', [])

        product = get_object_or_404(Product, id=product_uuid)

        updated = False
        for product_data in products:
            if product_data['id'] == str(product_uuid):
                product_data['units_purchased'] += units_purchased
                updated = True
                break

        if not updated:
            product_data = {
                'id': str(product_uuid),
                'units_purchased': units_purchased,
            }
            products.append(product_data)

        request.session['cart'] = cart

        updated_product_data = {
            'id': str(product.id),
            'units_purchased': product_data['units_purchased'],
            'name': product.name,
            'percentual_margin': product.percentual_margin,
            'cost_price': product.cost_price,
        }

        product_instance = Product.objects.get(id=product_uuid)
        product_serializer = ProductSerializer(
            product_instance, context={'request': request}
        )
        updated_product_data['price'] = product_serializer.data['price']
        updated_product_data[
            'post_discount_price'
        ] = product_serializer.get_post_discount_price(
            product_instance,
            updated_units_purchased=product_data['units_purchased'],
        )

        return Response(updated_product_data, status=status.HTTP_200_OK)


class HealthCheck(APIView):
    """
    Checks the API's health.
    """

    def get(self, request, *args, **kwargs):
        return Response({'status': 'ok'})


class CampaignDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = CampaignSerializer
    queryset = Campaign.objects.all()


class CampaignList(generics.ListCreateAPIView):
    serializer_class = CampaignSerializer
    queryset = Campaign.objects.all()


class PhotoDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = PhotoSerializer
    queryset = Photo.objects.all()


class PhotoList(generics.ListCreateAPIView):
    serializer_class = PhotoSerializer
    queryset = Photo.objects.all()


class ProductDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ProductSerializer
    queryset = Product.objects.all()


class ProductList(generics.ListCreateAPIView):
    serializer_class = ProductSerializer
    queryset = Product.objects.all()


class TypeDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = TypeSerializer
    queryset = Type.objects.all()


class TypeList(generics.ListCreateAPIView):
    serializer_class = TypeSerializer
    queryset = Type.objects.all()
