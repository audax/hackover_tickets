import pytest
from django.urls import reverse
from . import models as m


@pytest.mark.django_db
def test_order_merchandise_list(webuser, merchandise_factory):
    merch = [merchandise_factory() for _ in range(5)]
    response = webuser.get(reverse('merch_order'))
    for item in merch:
        assert item.name in response


@pytest.mark.django_db
def test_order_merchandise(webuser, user, merchandise_factory):
    merch = [merchandise_factory() for _ in range(5)]
    form = webuser.get(reverse('merch_order')).form
    for i in range(len(merch)):
        form['form-{}-amount'.format(i)] = i
    response = form.submit()
    assert response.status_code == 201
    order = m.MerchandiseOrder.objects.filter(owner=user).first()
    assert not order.paid
    for item in merch:
        assert item in [order_part.merchandise for order_part in order.items.all()]
