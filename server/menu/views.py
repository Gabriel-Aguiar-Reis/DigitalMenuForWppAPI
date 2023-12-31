from decimal import Decimal
import uuid
from django.contrib.sessions.models import Session
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


class AddToCart(APIView):
    def patch(self, request, pk, units, *args, **kwargs):
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
                product_data['units'] += units
                updated = True
                break

        if not updated:
            product_data = {
                'id': str(product_uuid),
                'units': units,
            }
            products.append(product_data)

        request.session['cart'] = cart

        updated_product_data = {
            'id': str(product.id),
            'units': product_data['units'],
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
            updated_units=product_data['units'],
        )

        return Response(updated_product_data, status=status.HTTP_200_OK)


class RemoveFromCart(APIView):
    def patch(self, request, pk, units, *args, **kwargs):
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
                product_data['units'] -= units
                updated = True
                break

        if updated and product_data['units'] <= 0:
            products.remove(product_data)

        request.session['cart'] = cart
        if updated and product_data['units'] >= 0:
            updated_product_data = {
                'id': str(product.id),
                'units': product_data['units'],
                'name': product.name,
                'percentual_margin': product.percentual_margin,
                'cost_price': product.cost_price,
            }

        product_instance = Product.objects.get(id=product_uuid)
        product_serializer = ProductSerializer(
            product_instance, context={'request': request}
        )
        if updated and product_data['units'] >= 0:
            updated_product_data['price'] = product_serializer.data['price']
            updated_product_data[
                'post_discount_price'
            ] = product_serializer.get_post_discount_price(
                product_instance, updated_units=product_data['units']
            )
            return Response(updated_product_data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_204_NO_CONTENT)


class ClearCart(APIView):
    def delete(self, request, *args, **kwargs):

        session_key = request.session.session_key
        if session_key:

            if 'cart' in request.session:
                del request.session['cart']

            return Response(status=status.HTTP_204_NO_CONTENT)

        return Response(
            {'detail': 'No cart to clear'}, status=status.HTTP_404_NOT_FOUND
        )


class ViewCart(APIView):
    def get(self, request, *args, **kwargs):

        session_key = request.session.session_key
        if session_key:

            cart = request.session.get('cart', {'products': []})
            products = cart.get('products', [])

            cart_data = {'products': []}

            for product_data in products:
                product_instance = Product.objects.get(id=product_data['id'])
                product_serializer = ProductSerializer(
                    product_instance, context={'request': request}
                )
                if product_serializer.data['size'] is not None:
                    cart_data['products'].append(
                        {
                            'id': str(product_instance.id),
                            'type': product_serializer.data['type'],
                            'name': product_serializer.data['name'],
                            'promotion': product_serializer.data['promotion'],
                            'size': product_serializer.data['size'],
                            'units': product_data['units'],
                            'post_discount_price': product_serializer.get_post_discount_price(
                                product_instance,
                                updated_units=product_data['units'],
                            ),
                        }
                    )
                else:
                    cart_data['products'].append(
                        {
                            'id': str(product_instance.id),
                            'type': product_serializer.data['type'],
                            'name': product_serializer.data['name'],
                            'promotion': product_serializer.data['promotion'],
                            'units': product_data['units'],
                            'post_discount_price': product_serializer.get_post_discount_price(
                                product_instance,
                                updated_units=product_data['units'],
                            ),
                        }
                    )
                    
            return Response(cart_data, status=status.HTTP_200_OK)

        return Response(
            {'detail': 'No cart available'}, status=status.HTTP_404_NOT_FOUND
        )


class AddIngredient(APIView):
    def post(self, request, *args, **kwargs):
        product_uuid = kwargs.get('pk')
        name = kwargs.get('name')
        price = float(kwargs.get('price'))

        try:
            product = Product.objects.get(id=product_uuid)
        except Product.DoesNotExist:
            return Response({'error': 'Product not found.'}, status=status.HTTP_404_NOT_FOUND)

        ingredient_id = str(uuid.uuid4())

        new_ingredient = {
            'id': ingredient_id,
            'name': name,
            'qty': 0,
            'price': price
        }

        product.ingredients.append(new_ingredient)
        product.save()

        serializer = ProductSerializer(product)
        return Response(serializer.data, status=status.HTTP_200_OK)


class AddQtyToIngredient(APIView):
    def post(self, request, pk, ingredient_pk, qty_added, *args, **kwargs):
        product_uuid = pk
        ingredient_uuid = ingredient_pk
        qty_added = qty_added

        session_key = request.session.session_key
        if not session_key:
            request.session.create()
        
        cart = request.session.get('cart', {'products': []})
        products = cart.get('products', [])
        product = get_object_or_404(Product, id=product_uuid)
        
        updated = False
        for product_data in products:
            if product_data['id'] == str(product_uuid):
                ingredients = product_data['ingredients']
                
                for ingredient in ingredients:
                    if ingredient['id'] == str(ingredient_uuid):
                        ingredient['qty'] += qty_added
                        updated = True
                        
        if not updated:
            product_data = {
                'id': str(product_uuid),
                'ingredients': [
                    {
                        'id': str(ingredient_uuid),
                        'qty': qty_added
                    }
                ]
            }
            products.append(product_data)
            
        request.session['cart'] = cart
        
        ingredient_data = next(
            (ingredient for ingredient in product_data['ingredients'] if ingredient['id'] == str(ingredient_uuid)),
            None
        )
        if ingredient_data:
            updated_product_data = {
                'id': str(product.id),
                'units': product.units,
                'name': product.name,
                'percentual_margin': product.percentual_margin,
                'cost_price': product.cost_price,
                'ingredients': [{
                    'id': ingredient_data['id'],
                    'qty': ingredient_data['qty']
                }],
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
            updated_units=product.units,
        )

        return Response(updated_product_data, status=status.HTTP_200_OK)


class RemoveIngredient(APIView):
    def delete(self, request, *args, **kwargs):
        product_uuid = str(kwargs.get('pk'))
        ingredient_uuid = str(kwargs.get('ingredient_pk'))

        try:
            product = Product.objects.get(id=product_uuid)
        except Product.DoesNotExist:
            return Response({'error': 'Product not found.'}, status=status.HTTP_404_NOT_FOUND)

        ingredient_index = None
        for i, ingredient in enumerate(product.ingredients):
            if ingredient['id'] == ingredient_uuid:
                ingredient_index = i
                break

        if ingredient_index is not None:
            del product.ingredients[ingredient_index]
            product.save()
            serializer = ProductSerializer(product)
            return Response(serializer.data, status=status.HTTP_204_NO_CONTENT)

        else:
            return Response({'error': 'Ingredient not found in the product.'}, status=status.HTTP_404_NOT_FOUND)


class ListIngredients(APIView):
    def get(self, request, *args, **kwargs):
        product_uuid = kwargs.get('pk')

        try:
            product = Product.objects.get(id=product_uuid)
        except Product.DoesNotExist:
            return Response({'error': 'Product not found.'}, status=status.HTTP_404_NOT_FOUND)

        ingredients = product.ingredients

        ingredients = [{'id': i['id'],'name': i['name'], 'qty': i['qty'], 'price': i['price']} for i in product.ingredients]

        return Response({'ingredients': ingredients}, status=status.HTTP_200_OK)


class GetIngredient(APIView):
    def get(self, request, pk, ingredient_pk, *args, **kwargs):
        product_uuid = pk
        ingredient_uuid = ingredient_pk
        
        try:
            product = Product.objects.get(id=product_uuid)
        except Product.DoesNotExist:
            return Response({'error': 'Product not found.'}, status=status.HTTP_404_NOT_FOUND)
        ingredient = None
        ingredients = product.ingredients
        for ing in ingredients:
            if str(ing['id']) == str(ingredient_uuid):
                ingredient = ing
                break

        return Response({'ingredient': ingredient}, status=status.HTTP_200_OK)


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
