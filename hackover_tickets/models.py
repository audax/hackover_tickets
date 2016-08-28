import uuid
from django.db import models
from django.contrib.auth.models import User


class Merchandise(models.Model):
    name = models.TextField()
    price = models.DecimalField(decimal_places=2, max_digits=20)

    def __str__(self):
        return "{} - {}".format(self.name, self.price)


class AbstractOrder(models.Model):
    order_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    paid = models.BooleanField(default=False)
    accessed = models.BooleanField(default=False)
    owner = models.ForeignKey(User, editable=False)

    class Meta:
        abstract = True


class MerchandiseOrder(AbstractOrder):

    @property
    def total_price(self):
        return sum(item.amount * item.merchandise.price for item in self.items.all())


class OrderRelation(models.Model):
    merchandise = models.ForeignKey(Merchandise, editable=False)
    amount = models.PositiveIntegerField(editable=False)
    order = models.ForeignKey(MerchandiseOrder, related_name='items', editable=False)


class TicketType(models.Model):
    name = models.TextField()
    price = models.DecimalField(decimal_places=2, max_digits=20)
    public = models.BooleanField()


class Ticket(AbstractOrder):
    type = models.ForeignKey(TicketType, editable=False)
