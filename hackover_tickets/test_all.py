import pytest
from . import models as m


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


@pytest.mark.django_db
def test_order_ticket_form(user_client, ticket_type):
    response = user_client.get('/tickets/order')
    assert response.status_code == 200
    assert ticket_type.name in response.content.decode('utf-8')


@pytest.mark.django_db
def test_order_ticket(user_client, user, ticket_type):
    response = user_client.post('/tickets/order', {'ticket_type': ticket_type.id})
    assert ticket_type.name in response.content.decode('utf-8')
    ticket = m.Ticket.objects.get(owner=user)
    assert ticket.type == ticket_type
    assert ticket.order_id
