import datetime
import factory
import factory.django
import pytest
from factory.django import DjangoModelFactory
from pytest_factoryboy import register
from django.conf import settings
from django.contrib.auth import models
from django.utils import timezone


def _get_tzinfo():
    if settings.USE_TZ:
        return timezone.get_current_timezone()
    else:
        return None


@register
class UserFactory(DjangoModelFactory):
    class Meta:
        model = models.User

    username = factory.Faker('user_name')
    first_name = factory.Faker('first_name')
    last_name = factory.Faker('last_name')
    email = factory.Faker('email')
    password = factory.PostGenerationMethodCall('set_password', 'password123')

    is_active = True
    is_staff = False
    is_superuser = False

    last_login = factory.LazyAttribute(
        lambda _o: datetime.datetime(2000, 1, 1, tzinfo=_get_tzinfo()))
    date_joined = factory.LazyAttribute(
        lambda _o: datetime.datetime(1999, 1, 1, tzinfo=_get_tzinfo()))


@pytest.mark.django_db
@pytest.fixture
def user_client(client, user):
    client.force_login(user)
    return client


