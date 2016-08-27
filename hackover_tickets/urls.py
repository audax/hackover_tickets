from django.conf.urls import url
from .views import index, ticket_order

urlpatterns = [
    url(r'^$', index, name='index'),
    url(r'^tickets/order$', ticket_order, name='ticket_order')
    ]
