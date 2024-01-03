from typing import Optional

from .models import Product, Type


class Util:
    @staticmethod
    def __is_valid(
        any_value: Optional[int] | Optional[float],
    ) -> (int | float):
        if any_value == None:
            any_value = 0
        return any_value

    @staticmethod
    def calculate_value_after_discount(
        price: Optional[float] = None,
        units: Optional[int] = None,
        discount_amount: Optional[int] = None,
        percentual_discount: Optional[float] = None,
        unit_discount: Optional[int] = None,
        amount_for_discount: Optional[float] = None,
        unit_for_discount: Optional[int] = None,
    ) -> float:

        parameters = [
            price,
            units,
            discount_amount,
            percentual_discount,
            unit_discount,
            amount_for_discount,
            unit_for_discount,
        ]

        valid_params = [Util.__is_valid(param) for param in parameters]

        [
            price,
            units,
            discount_amount,
            percentual_discount,
            unit_discount,
            amount_for_discount,
            unit_for_discount,
         ] = valid_params

        value: Optional[int | float] = price * units
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
                    discount_amount,
                    amount_for_discount,
                    value >= amount_for_discount,
                ),
                (
                    discount_amount,
                    unit_for_discount,
                    value >= (unit_for_discount * price),
                ),
                (
                    percentual_discount,
                    amount_for_discount,
                    value >= amount_for_discount,
                ),
                (
                    percentual_discount,
                    unit_for_discount,
                    value >= (unit_for_discount * price),
                ),
                (
                    unit_discount,
                    amount_for_discount,
                    value >= amount_for_discount,
                ),
                (
                    unit_discount,
                    unit_for_discount,
                    value >= (unit_for_discount * price),
                ),
            ]

            result = f'Invalid: Non-applicable discount.'
            for (
                discount_type,
                discount_validation,
                condition_met,
            ) in discount_conditions:
                if discount_type and discount_validation and condition_met:
                    if discount_type == discount_amount:
                        result = value - discount_amount
                    elif discount_type == percentual_discount:
                        result = value - (value * percentual_discount)
                    elif discount_type == unit_discount:
                        result = value - (unit_discount * price)
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
    ) -> float:

        parameters = [
            cost_price,
            product_percentual_margin,
            type_percentual_margin,
        ]

        valid_params = [Util.__is_valid(param) for param in parameters]

        (
            cost_price,
            product_percentual_margin,
            type_percentual_margin,
        ) = valid_params

        if product_percentual_margin != 0 and type_percentual_margin != 0:
            result = (
                cost_price
                + (cost_price * product_percentual_margin)
                + (cost_price * type_percentual_margin)
            )
        elif product_percentual_margin != 0 and type_percentual_margin == 0:
            result = cost_price + (cost_price * product_percentual_margin)
        elif type_percentual_margin != 0 and product_percentual_margin == 0:
            result = cost_price + (cost_price * type_percentual_margin)
        elif product_percentual_margin == 0 and type_percentual_margin:
            result = cost_price
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
        return type_data.percentual_margin
    
    @staticmethod
    def override_none_product_promo(obj):
        object = Product.objects.get(id=obj.id)
        type = object.type
        type_data = Type.objects.get(name=type)
        if (type_data.promotion != object.promotion
            and object.promotion is None):
            obj.promotion = type_data.promotion
        return obj.promotion