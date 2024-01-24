import ast
from django.forms import model_to_dict
from rest_framework import generics, status
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView

from .utils import Util

from .models import Campaign, Ingredient, Photo, Product, Type
from .serializers import (
    CampaignSerializer,
    IngredientSerializer,
    PhotoSerializer,
    ProductSerializer,
    TypeSerializer,
)

class CalculateTotalOrderPrice(APIView):
    def get(self, request, *args, **kwargs):
        session_key = request.session.session_key
        if not session_key:
            return Response({'error': 'Session key not found'}, status=status.HTTP_400_BAD_REQUEST)

        cart = request.session.get('cart', {'products': []})
        products = cart.get('products', [])

        total_order_price = 0
        for product_data in products:
            if 'promotion' in product_data:
                promo = product_data['promotion']
                if isinstance(promo, dict):
                    discount_amount = promo.get('discount_amount', 0)
                    percentual_discount = promo.get('percentual_discount', 0)
                    unit_discount = promo.get('unit_discount', 0)
                    amount_for_discount = promo.get('amount_for_discount', 0)
                    unit_for_discount = promo.get('unit_for_discount', 0)
                else:
                    discount_amount = 0
                    percentual_discount = 0
                    unit_discount = 0
                    amount_for_discount = 0
                    unit_for_discount = 0
            else:
                discount_amount = 0
                percentual_discount = 0
                unit_discount = 0
                amount_for_discount = 0
                unit_for_discount = 0

            post_discount_price = Util.calculate_value_after_discount(
                product_data['price'],
                product_data['units'],
                discount_amount,
                percentual_discount,
                unit_discount,
                amount_for_discount,
                unit_for_discount
            )
            
            if product_data['units'] > 0:
                if isinstance(post_discount_price, (float | int)):
                    total_order_price += post_discount_price
                else:
                    total_order_price += float(post_discount_price[-1])

                for ingredient in product_data.get('ingredients', []):
                    if ingredient['qty'] > 0:
                        total_order_price += float(ingredient['total_price'])
        cart['total_order_price'] = total_order_price
        request.session['cart'] = cart

        return Response({'total_order_price': total_order_price}, status=status.HTTP_200_OK)


class AddToCart(APIView):
    def patch(self, request, pk, units, *args, **kwargs):
        product_uuid = pk

        session_key = request.session.session_key
        if not session_key:
            request.session.create()

        cart = request.session.get('cart', {'products': []})
        products = cart.get('products', [])

        product = get_object_or_404(Product, id=product_uuid)
        
        
        product_serializer = ProductSerializer(
            product, context={'request': request}
        )
        
        print(product_serializer.data['ingredients'])

        updated = False
        
        for product_data in products:
            if product_data['id'] == str(product_uuid):
                product_data['units'] += units
                updated = True
                break
        
        price = str(Util.calculate_product_price(
            product.cost_price,
            product.percentual_margin,
            product.type.percentual_margin,
            product.ingredients
        ))
        
        post_discount_price = str(Util.calculate_value_after_discount(
            price,
            units,
            product.promotion.discount_amount if product.promotion is not None and product.promotion.discount_amount is not None else 0,
            product.promotion.percentual_discount if product.promotion is not None and product.promotion.percentual_discount is not None else 0,
            product.promotion.unit_discount if product.promotion is not None and product.promotion.unit_discount is not None else 0,
            product.promotion.amount_for_discount if product.promotion is not None and product.promotion.amount_for_discount is not None else 0,
            product.promotion.unit_for_discount if product.promotion is not None and product.promotion.unit_for_discount is not None else 0,
        ))
        
        type_data = model_to_dict(product.type)
        campaign_data = ""
        if product.promotion is not None:
            campaign_data = model_to_dict(product.promotion)
        
        
        if not updated:
            product_data = {
                'id': str(product_uuid),
                'units': units,
                'name': product.name,
                'percentual_margin': str(product.percentual_margin),
                'type': type_data,
                'promotion': campaign_data,
                'cost_price': str(product.cost_price),
                'ingredients': product_serializer.data['ingredients'],
                'price': price,
                'post_discount_price': post_discount_price,
            }
            products.append(product_data)

        request.session['cart'] = cart

        updated_product_data = {
            'id': str(product_uuid),
            'units': product_data['units'],
            'name': product.name,
            'percentual_margin': str(product.percentual_margin),
            'type': type_data,
            'promotion': campaign_data,
            'ingredients': product_serializer.data['ingredients'],
            'cost_price': str(product.cost_price),
            'price': price,
            'post_discount_price': post_discount_price,
        }

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

            updated_product_data['price'] = product_serializer.data['price']
            updated_product_data[
                'post_discount_price'
            ] = product_serializer.get_post_discount_price(
                product_instance, updated_units=product_data['units']
            )

            return Response(updated_product_data, status=status.HTTP_200_OK)
        
        return Response(status=status.HTTP_204_NO_CONTENT)


class AddQtyToIngredient(APIView):
    def patch(self, request, pk, ingredient_pk, qty_added, *args, **kwargs):
        product_uuid = pk
        ingredient_uuid = ingredient_pk
        qty_added = qty_added

        session_key = request.session.session_key
        if not session_key:
            request.session.create()

        cart = request.session.get('cart', {'products': []})
        products = cart.get('products', [])
        product = get_object_or_404(Product, id=str(product_uuid))
        ingredient = get_object_or_404(Ingredient, id=str(ingredient_uuid))
        product_serializer = ProductSerializer(
            product, context={'request': request}
        )

        updated = False
        for product_data in products:
            if product_data['id'] == str(product_uuid):
                if 'ingredients' not in product_data:
                    product_data['ingredients'] = []

                for ingredient_data in product_data['ingredients']:
                    ingredient_data['price'] = Util.calculate_ingredient_price(ingredient_data['cost_price'], ingredient_data['percentual_margin'])
                    if ingredient_data['id'] == str(ingredient_uuid):
                        ingredient_data['qty'] += qty_added
                        updated = True
                    ingredient_data['total_price'] = ingredient_data['price'] * ingredient_data['qty']

                if not updated:
                    price = Util.calculate_ingredient_price(ingredient.cost_price, ingredient.percentual_margin)
                    new_ingredient_data = {
                        'id': str(ingredient_uuid),
                        'qty': qty_added,
                        'price': price,
                        'total_price': (price * qty_added)
                    }
                    product_data['ingredients'].append(new_ingredient_data)

        if not updated:
            price = Util.calculate_ingredient_price(ingredient.cost_price, ingredient.percentual_margin)
            product_data = {
                'id': str(product_uuid),
                'units': 1,
                'name': product.name,
                'promotion': str(product_serializer.data['promotion'] if product_serializer.data['promotion'] is not None else ''),
                'type': str(product_serializer.data['type'] if product_serializer.data['type'] is not None else ''),
                'percentual_margin': product.percentual_margin,
                'cost_price': product.cost_price,
                'price': product_serializer.data['price'],
                'post_discount_price': product_serializer.get_post_discount_price(
                    product,
                    updated_units=product.units,
                ),
                'ingredients': [
                    {
                        'id': str(ingredient_uuid),
                        'qty': qty_added,
                        'price': price,
                        'total_price': (price * qty_added)
                    }
                ]
            }
            products.append(product_data)

        request.session['cart'] = cart


        updated_product_data = {
            'id': str(product.id),
            'units': product_data['units'],
            'name': product.name,
            'promotion': str(product_serializer.data['promotion'] if product_serializer.data['promotion'] is not None else ''),
            'type': str(product_serializer.data['type'] if product_serializer.data['type'] is not None else ''),
            'percentual_margin': product.percentual_margin,
            'cost_price': product.cost_price,
            'ingredients': product_data['ingredients'],
            'price': product_serializer.data['price'],
            'post_discount_price': product_serializer.get_post_discount_price(
                product,
                updated_units=product_data['units'],
            ),
        }

        return Response(updated_product_data, status=status.HTTP_200_OK)


class RemoveQtyFromIngredient(APIView):
    def patch(self, request, pk, ingredient_pk, qty_removed, *args, **kwargs):
        product_uuid = pk
        ingredient_uuid = ingredient_pk
        qty_removed = qty_removed

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
                    if ingredient['qty'] >= qty_removed:
                        ingredient['qty'] -= qty_removed
                        updated = True
                    else:
                        ingredient['qty'] = 0
                        updated = True

        if not updated:
            price = Util.calculate_ingredient_price(ingredient.cost_price, ingredient.percentual_margin)
            product_data = {
                'id': str(product_uuid),
                'ingredients': [
                    {
                        'id': str(ingredient_uuid),
                        'qty': 0,
                        'price': price,
                        'total_price': (price * 0)
                    }
                ]
            }
            products.append(product_data)

        request.session['cart'] = cart

        ingredient_data = next(
            (ingredient for ingredient in product_data['ingredients'] if ingredient['id'] == str(ingredient_uuid)),
            None
        )
        product_data = next(
            (product for product in products if product['id'] == str(product_uuid)),
            None
        )
        if ingredient_data:
            updated_product_data = {
                'id': str(product.id),
                'units': product_data['units'],
                'name': product.name,
                'percentual_margin': product.percentual_margin,
                'cost_price': product.cost_price,
                'ingredients': [{
                    'id': ingredient_data['id'],
                    'qty': ingredient_data['qty'],
                    'price': ingredient_data['price'],
                    'total_price': (ingredient_data['price'] * ingredient_data['qty'])
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
        else:
            return Response({'error': 'Ingredient not found'}, status=status.HTTP_404_NOT_FOUND)


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

                cart_product_data = {
                    'id': str(product_instance.id),
                    'type': product_serializer.data['type'],
                    'price': product_serializer.data['price'],
                    'cost_price': product_serializer.data['cost_price'],
                    'name': product_serializer.data['name'],
                    'promotion': product_serializer.data['promotion'],
                    'units': product_data.get('units'),
                    'post_discount_price': product_serializer.get_post_discount_price(
                        product_instance,
                        updated_units=product_data.get('units'),
                    ),
                }

                if 'ingredients' in product_data:
                    cart_product_data['ingredients'] = product_data['ingredients']

                if product_serializer.data['size'] is not None:
                    cart_product_data['size'] = product_serializer.data['size']

                cart_data['products'].append(cart_product_data)

            return Response(cart_data, status=status.HTTP_200_OK)

        cart = request.session.get('cart', {'products': []})
        return Response(cart, status=status.HTTP_200_OK)


class HealthCheck(APIView):
    """
    Checks the API's health.
    """

    def get(self, request, *args, **kwargs):
        return Response({'status': 'ok'})


class IngredientList(generics.ListCreateAPIView):
    serializer_class = IngredientSerializer
    queryset = Ingredient.objects.all()
    
    
class IngredientDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = IngredientSerializer
    queryset = Ingredient.objects.all()


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
