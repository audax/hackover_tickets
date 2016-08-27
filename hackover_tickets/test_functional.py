import pytest
from django.urls import reverse


@pytest.mark.django_db
def test_order_merchandise_list(webuser, merchandise_factory):
    merch = [merchandise_factory() for _ in range(5)]
    response = webuser.get(reverse('merch_order'))
    for item in merch:
        assert item.name in response
