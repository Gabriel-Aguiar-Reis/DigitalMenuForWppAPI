from menu.utils import Util


def test_discount_amount_by_amount():
    assert (
        Util.calculate_value_after_discount(
            price=20,
            units=3,
            discount_amount=10,
            percentual_discount=None,
            unit_discount=None,
            amount_for_discount=60,
            unit_for_discount=None,
        )
        == 50
    )


def test_discount_amount_by_unit():
    assert (
        Util.calculate_value_after_discount(
            price=40,
            units=4,
            discount_amount=10,
            percentual_discount=None,
            unit_discount=None,
            amount_for_discount=None,
            unit_for_discount=4,
        )
        == 150
    )


def test_percentual_discount_by_amount():
    assert (
        Util.calculate_value_after_discount(
            price=1,
            units=30,
            discount_amount=None,
            percentual_discount=0.2,
            unit_discount=None,
            amount_for_discount=20,
            unit_for_discount=None,
        )
        == 24.0
    )


def test_percentual_discount_by_unit():
    assert (
        Util.calculate_value_after_discount(
            price=50,
            units=3,
            discount_amount=None,
            percentual_discount=0.1,
            unit_discount=None,
            amount_for_discount=None,
            unit_for_discount=3,
        )
        == 135.0
    )


def test_unit_discount_by_amount():
    assert (
        Util.calculate_value_after_discount(
            price=5,
            units=30,
            discount_amount=None,
            percentual_discount=None,
            unit_discount=5,
            amount_for_discount=20,
            unit_for_discount=None,
        )
        == 125
    )


def test_unit_discount_by_unit():
    assert (
        Util.calculate_value_after_discount(
            price=25,
            units=3,
            discount_amount=None,
            percentual_discount=None,
            unit_discount=1,
            amount_for_discount=None,
            unit_for_discount=3,
        )
        == 50
    )


def test_no_value_reported():
    assert (
        Util.calculate_value_after_discount(
            price=None,
            units=None,
            discount_amount=None,
            percentual_discount=None,
            unit_discount=None,
            amount_for_discount=None,
            unit_for_discount=None,
        )
        == 'Invalid: There is no value reported.'
    )


def test_non_applicable_discount():
    assert (
        Util.calculate_value_after_discount(
            price=20,
            units=3,
            discount_amount=10,
            percentual_discount=None,
            unit_discount=None,
            amount_for_discount=None,
            unit_for_discount=6,
        )
        == 'Invalid: Non-applicable discount.'
    )


def test_wrong_discount_config():
    assert (
        Util.calculate_value_after_discount(
            price=50,
            units=4,
            discount_amount=None,
            percentual_discount=0.1,
            unit_discount=None,
            amount_for_discount=20,
            unit_for_discount=2,
        )
        == 'Invalid: Wrong Discount Configuration.'
    )


def test_purchase_value_equals_480():
    assert (
        Util.calculate_value_after_discount(
            price=60,
            units=10,
            discount_amount=None,
            percentual_discount=None,
            unit_discount=2,
            amount_for_discount=None,
            unit_for_discount=10,
        )
        == 480
    )


def test_product_price_equals_0():
    assert (
        Util.calculate_product_price(
            cost_price=None,
            product_percentual_margin=None,
            type_percentual_margin=None,
        )
        == 0
    )


def test_product_price_equals_44():
    assert (
        Util.calculate_product_price(
            cost_price=40,
            product_percentual_margin=0.10,
            type_percentual_margin=None,
        )
        == 44
    )


def test_product_price_equals_11_5():
    assert (
        Util.calculate_product_price(
            cost_price=10,
            product_percentual_margin=None,
            type_percentual_margin=0.15,
        )
        == 11.5
    )


def test_product_price_equals_25():
    assert (
        Util.calculate_product_price(
            cost_price=20,
            product_percentual_margin=0.05,
            type_percentual_margin=0.20,
        )
        == 25
    )
