import uuid
from django.db import models
from django.contrib.auth.models import User


class Merchandise(models.Model):
    name = models.TextField()
    price = models.DecimalField(decimal_places=2, max_digits=20)


class MerchandiseOrder(models.Model):
    order_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    owner = models.ForeignKey(User)


class OrderRelation(models.Model):
    merchandise = models.ForeignKey(Merchandise)
    amount = models.PositiveIntegerField()
    order = models.ForeignKey(MerchandiseOrder)


class TicketType(models.Model):
    name = models.TextField()
    price = models.DecimalField(decimal_places=2, max_digits=20)
    public = models.BooleanField()


class Ticket(models.Model):
    order_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    type = models.ForeignKey(TicketType)
    owner = models.ForeignKey(User)
    paid = models.BooleanField(default=False)
    accessed = models.BooleanField(default=False)
