from django.conf.urls import url
from .views import index, ticket_order, ticket_list

urlpatterns = [
    url(r'^$', index, name='index'),
    url(r'^tickets/order$', ticket_order, name='ticket_order'),
    url(r'^tickets/list$', ticket_list, name='ticket_list'),
    ]
