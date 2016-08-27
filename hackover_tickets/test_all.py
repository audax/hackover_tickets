import pytest


@pytest.mark.django_db
def test_wearable_defaults(wearable):
    assert wearable.price > 0
    assert wearable.name


@pytest.mark.django_db
def test_wearable(wearable, order_relation):
    assert wearable.price == order_relation.wearable.price
    assert wearable.name == order_relation.wearable.name
    assert order_relation.amount > 0
