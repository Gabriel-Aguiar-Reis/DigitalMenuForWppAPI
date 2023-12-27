from rest_framework import generics, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from menu.models import Campaign, Photo, Product, Type
from menu.serializers import (
    CampaignSerializer,
    PhotoSerializer,
    ProductSerializer,
    TypeSerializer,
)

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    @action(detail=True, methods=['post'])
    def update_units_purchased(self, request, pk=None):
        product = self.get_object()
        units_purchased = request.data.get('units_purchased')

        request.units_purchased = units_purchased

        serializer = self.get_serializer(product)
        return Response(serializer.data)

class HealthCheckView(generics.ListAPIView):
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
