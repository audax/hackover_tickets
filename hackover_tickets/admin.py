from django.contrib import admin
from . import models as m

for model in (m.Merchandise, m.TicketType, m.Ticket):
    admin.site.register(model)
