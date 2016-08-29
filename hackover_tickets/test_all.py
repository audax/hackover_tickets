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
    assert _("unpaid") in content


@pytest.mark.django_db
def test_qrcode(ticket):
    with pytest.raises(ValueError):
        assert ticket.qrcode.url
    ticket.generate_qrcode()
    assert ticket.qrcode.url is not None


@pytest.mark.django_db
def test_show_ticket_denied(user_client, ticket):
    assert not ticket.paid
    assert not ticket.accessed
    response = user_client.get(ticket.get_absolute_url())
    assert response.status_code == 403
    assert _("unpaid") in response.content.decode('utf-8')
    assert ticket == response.context['ticket']
    assert not ticket.accessed


@pytest.mark.django_db
def test_show_ticket(user_client, ticket):
    ticket.paid = True
    ticket.save()
    response = user_client.get(ticket.get_absolute_url())
    assert response.status_code == 200
    ticket.refresh_from_db()
    assert ticket.accessed
    assert str(ticket.order_id) in response.content.decode('utf-8')


@pytest.mark.django_db
def test_show_order_denied(user_client, order_relation):
    order = order_relation.order
    assert not order.paid
    assert not order.accessed
    response = user_client.get(order.get_absolute_url())
    assert response.status_code == 403
    assert _("unpaid") in response.content.decode('utf-8')
    assert order == response.context['order']
    assert not order.accessed


@pytest.mark.django_db
def test_show_order(user_client, order_relation):
    order = order_relation.order
    order.paid = True
    order.save()
    response = user_client.get(order.get_absolute_url())
    order.refresh_from_db()
    assert order.accessed
    assert order == response.context['order']
    assert str(order.order_id) in response.content.decode('utf-8')


