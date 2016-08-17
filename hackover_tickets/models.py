import uuid
from django.db import models
from django.contrib.auth.models import User


class Wearable(models.Model):
    name = models.TextField()
    price = models.DecimalField(decimal_places=2, max_digits=20)


class WearableOrder(models.Model):
    order_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    owner = models.ForeignKey(User)


class OrderRelation(models.Model):
    wearable = models.ForeignKey(Wearable)
    amount = models.PositiveIntegerField()
    order = models.ForeignKey(WearableOrder)


class TicketType(models.Model):
    name = models.TextField()
    price = models.DecimalField(decimal_places=2, max_digits=20)
    public = models.BooleanField()


class Ticket(models.Model):
    order_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    type = models.ForeignKey(TicketType)
    owner = models.ForeignKey(User)
