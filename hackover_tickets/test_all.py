import pytest


@pytest.mark.django_db
def test_merchandise_defaults(merchandise):
    assert merchandise.price > 0
    assert merchandise.name


@pytest.mark.django_db
def test_merchandise(merchandise, order_relation):
    assert merchandise.price == order_relation.merchandise.price
    assert merchandise.name == order_relation.merchandise.name
    assert order_relation.amount > 0


def test_redirect_to_register(client):
    assert 302 == client.get('/').status_code
