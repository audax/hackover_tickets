from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import url
from .views import index, ticket_order, ticket_list, ticket_show, merch_order, merch_list, merch_show

urlpatterns = [
    url(r'^$', index, name='index'),
    url(r'^tickets/order/$', ticket_order, name='ticket_order'),
    url(r'^tickets/list/$', ticket_list, name='ticket_list'),
    url(r'^tickets/show/(?P<order_id>[^/]+)/$', ticket_show, name='ticket_show'),
    url(r'^merchandise/order/$', merch_order, name='merch_order'),
    url(r'^merchandise/list/$', merch_list, name='merch_list'),
    url(r'^merchandise/show/(?P<order_id>[^/]+)/$', merch_show, name='merch_show'),
    ]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
