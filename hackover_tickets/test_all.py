import pytest

@pytest.mark.django_db
def test_login(user, user_client):
    assert user.username

