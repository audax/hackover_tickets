import pytest
from django.urls import reverse
from . import models as m
from django.utils.translation import ugettext as _


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
    response = user_client.get(reverse('ticket_order'))
    assert response.status_code == 200
    assert ticket_type.name in response.content.decode('utf-8')


@pytest.mark.django_db
def test_order_ticket(user_client, user, ticket_type):
    response = user_client.post(reverse('ticket_order'), {'ticket_type': ticket_type.id})
    assert ticket_type.name in response.content.decode('utf-8')
    ticket = m.Ticket.objects.get(owner=user)
    assert not ticket.paid
    assert not ticket.accessed
    assert ticket.type == ticket_type
    assert ticket.order_id


@pytest.mark.django_db
def test_list_tickets(user_client, user, ticket_factory):
    tickets = (ticket_factory(owner=user), ticket_factory(owner=user), ticket_factory(owner=user))
    response = user_client.get(reverse('ticket_list'))
    content = response.content.decode('utf-8')
    assert set(tickets) == set(response.context['tickets'])
    assert all(str(t.order_id) not in content for t in tickets)
    assert _("unpaid") in content
    assert _("ticket not accessed") in content
    assert _("accessed ticket") not in content


@pytest.mark.django_db
def test_order_merchandise_list(user_client, merchandise_factory):
    merch = [merchandise_factory() for _ in range(5)]
    response = user_client.get(reverse('merch_order'))
    content = response.content.decode('utf-8')
    for item in merch:
        assert item.name in content


@pytest.mark.django_db
def test_merchandise_order_price(merchandise_order):
    assert merchandise_order.total_price == 0


@pytest.mark.django_db
def test_merchandise_order_price_sum(merchandise_order, merchandise):
    order_relation = m.OrderRelation.objects.create(order=merchandise_order, merchandise=merchandise, amount=2)
    assert set(merchandise_order.items.all()) == {order_relation}
    assert merchandise_order.total_price == order_relation.merchandise.price * order_relation.amount


@pytest.mark.django_db
def test_list_merch_orders(user_client, user, merchandise_order_factory):
    orders = (merchandise_order_factory(owner=user), merchandise_order_factory(owner=user))
    response = user_client.get(reverse('merch_list'))
    content = response.content.decode('utf-8')
    assert set(orders) == set(response.context['orders'])
    for order in orders:
        assert str(order.order_id) not in content
    assert _("unpaid") in content
