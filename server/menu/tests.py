from menu.utils import Util


def test_discount_amount_by_amount():
    assert (
        Util.calculate_value_after_discount(
            value=100,
            unit_price=None,
            discount_amount=10,
            percentual_discount=None,
            unit_discount=None,
            amount_for_discount=60,
            unit_for_discount=None,
        )
        == 90
    )


def test_discount_amount_by_unit():
    assert (
        Util.calculate_value_after_discount(
            value=120,
            unit_price=30,
            discount_amount=10,
            percentual_discount=None,
            unit_discount=None,
            amount_for_discount=None,
            unit_for_discount=4,
        )
        == 110
    )


def test_percentual_discount_by_amount():
    assert (
        Util.calculate_value_after_discount(
            value=30,
            unit_price=None,
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
            value=150,
            unit_price=30,
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
            value=150,
            unit_price=40,
            discount_amount=None,
            percentual_discount=None,
            unit_discount=1,
            amount_for_discount=20,
            unit_for_discount=None,
        )
        == 110
    )


def test_unit_discount_by_unit():
    assert (
        Util.calculate_value_after_discount(
            value=50,
            unit_price=10,
            discount_amount=None,
            percentual_discount=None,
            unit_discount=1,
            amount_for_discount=None,
            unit_for_discount=3,
        )
        == 40
    )


def test_no_value_reported():
    assert (
        Util.calculate_value_after_discount(
            value=None,
            unit_price=None,
            discount_amount=None,
            percentual_discount=None,
            unit_discount=None,
            amount_for_discount=None,
            unit_for_discount=None,
        )
        == 'Invalid: There is no value reported.'
    )


def test_wrong_discount_config():
    assert (
        Util.calculate_value_after_discount(
            value=50,
            unit_price=20,
            discount_amount=10,
            percentual_discount=None,
            unit_discount=None,
            amount_for_discount=None,
            unit_for_discount=6,
        )
        == 'Invalid: Non-applicable discount.'
    )


def test_non_applicable_discount():
    assert (
        Util.calculate_value_after_discount(
            value=200,
            unit_price=None,
            discount_amount=None,
            percentual_discount=0.1,
            unit_discount=None,
            amount_for_discount=20,
            unit_for_discount=2,
        )
        == 'Invalid: Wrong Discount Configuration.'
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
