from typing import Optional, Union

from .models import Product, Type


class Util:
    @staticmethod
    def is_valid(any_value: Optional[Union[int, float, str]]) -> Union[int, float]:
        if any_value is None:
            any_value = 0
        elif isinstance(any_value, str):
            any_value = float(any_value)
        return any_value


    @staticmethod
    def calculate_ingredient_price(
        cost_price: Optional[float] = None,
        percentual_margin: Optional[float] = None,
    ) -> float:
        
        parameters = [
            cost_price,
            percentual_margin
        ]
        valid_params = [Util.is_valid(param) for param in parameters]
        
        if valid_params[1]:
            return valid_params[0] * (1 + (valid_params[1]/100))
        return valid_params[0]
    
    @staticmethod
    def calculate_value_after_discount(
        price: Optional[float | str] = None,
        units: Optional[int] = None,
        discount_amount: Optional[int | str] = None,
        percentual_discount: Optional[float | str] = None,
        unit_discount: Optional[int | str] = None,
        amount_for_discount: Optional[float | str] = None,
        unit_for_discount: Optional[int | str] = None,
    ) -> any:

        parameters = [
            price,
            units,
            discount_amount,
            percentual_discount,
            unit_discount,
            amount_for_discount,
            unit_for_discount,
        ]

        valid_params = [Util.is_valid(param) for param in parameters]

        
        price_valid, units_valid, discount_amount_valid, percentual_discount_valid, unit_discount_valid, amount_for_discount_valid, unit_for_discount_valid = valid_params

        value: Optional[float] = float(price_valid * units_valid)
        if not value:
            result = 'Invalid: There is no value reported.'
        elif (
            sum(1 for param in valid_params[2:5] if param != 0) != 1
            or sum(1 for param in valid_params[5:] if param != 0) != 1
        ):
            result = 'Invalid: Wrong Discount Configuration.'
        else:
            discount_conditions = [
                (
                    discount_amount_valid,
                    amount_for_discount_valid,
                    value >= amount_for_discount_valid,
                ),
                (
                    discount_amount_valid,
                    unit_for_discount_valid,
                    value >= (unit_for_discount_valid * price_valid),
                ),
                (
                    percentual_discount_valid,
                    amount_for_discount_valid,
                    value >= amount_for_discount_valid,
                ),
                (
                    percentual_discount_valid,
                    unit_for_discount_valid,
                    value >= (unit_for_discount_valid * price_valid),
                ),
                (
                    unit_discount_valid,
                    amount_for_discount_valid,
                    value >= amount_for_discount_valid,
                ),
                (
                    unit_discount_valid,
                    unit_for_discount_valid,
                    value >= (unit_for_discount_valid * price_valid),
                ),
            ]

            result = f'Invalid: Non-applicable discount.'
            for (
                discount_type,
                discount_validation,
                condition_met,
            ) in discount_conditions:
                if discount_type and discount_validation and condition_met:
                    if discount_type == discount_amount_valid:
                        result = value - discount_amount_valid
                    elif discount_type == percentual_discount_valid:
                        result = value - (value * (percentual_discount_valid/100))
                    elif discount_type == unit_discount_valid:
                        result = value - (unit_discount_valid * price_valid)
                    break

        if isinstance(result, str):
            return result, value
        else:
            return result

    @staticmethod
    def calculate_product_price(
        cost_price: Optional[float] = None,
        product_percentual_margin: Optional[float] = None,
        type_percentual_margin: Optional[float] = None,
        ingredients: any = None
    ) -> float:

        parameters = [
            cost_price,
            product_percentual_margin,
            type_percentual_margin,
        ]

        valid_params = [Util.is_valid(param) for param in parameters]

        (
            cost_price_valid,
            product_percentual_margin_valid,
            type_percentual_margin_valid,
        ) = valid_params

        if product_percentual_margin_valid != 0 and type_percentual_margin_valid != 0:
            for ingredient in ingredients.all():
                if ingredient.qty > 0:
                    cost_price_valid += ingredient.qty * ingredient.price
            result = (
                cost_price_valid
                + (cost_price_valid * (product_percentual_margin_valid/100))
                + (cost_price_valid * (type_percentual_margin_valid/100))
            )
        elif product_percentual_margin_valid != 0 and type_percentual_margin_valid == 0:
            for ingredient in ingredients.all():
                if ingredient.qty > 0:
                    cost_price_valid += ingredient.qty * ingredient.price
            result = cost_price_valid + (cost_price_valid * (product_percentual_margin_valid/100))
        elif type_percentual_margin_valid != 0 and product_percentual_margin_valid == 0:
            for ingredient in ingredients.all():
                if ingredient.qty > 0:
                    cost_price_valid += ingredient.qty * ingredient.price
            result = cost_price_valid + (cost_price_valid * (type_percentual_margin_valid/100))
        elif product_percentual_margin_valid == 0 and type_percentual_margin_valid == 0:
            for ingredient in ingredients.all():
                if ingredient.qty > 0:
                    cost_price_valid += ingredient.qty * ingredient.price
            result = cost_price_valid
        else:
            result = 0
        return result
    
    @staticmethod
    def get_type_percentual_margin(
        product_id: Optional[str] = None
    ) -> float:
        object = Product.objects.get(id=product_id)
        type = object.type
        type_data = Type.objects.get(name=type)
        if type_data is not None:
            return type_data.percentual_margin
        return None
    
    @staticmethod
    def override_none_product_promo(obj):
        object = Product.objects.get(id=obj.id)
        type = object.type
        type_data = Type.objects.get(name=type)
        if (type_data.promotion != object.promotion
            and object.promotion is None):
            obj.promotion = type_data.promotion
        return obj.promotion