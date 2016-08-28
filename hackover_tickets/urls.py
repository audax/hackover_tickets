from django.conf.urls import url
from .views import index, ticket_order, ticket_list, merch_order, merch_list

urlpatterns = [
    url(r'^$', index, name='index'),
    url(r'^tickets/order/$', ticket_order, name='ticket_order'),
    url(r'^tickets/list/$', ticket_list, name='ticket_list'),
    url(r'^merchandise/order/$', merch_order, name='merch_order'),
    url(r'^merchandise/list/$', merch_list, name='merch_list'),
    ]
