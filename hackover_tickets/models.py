import uuid
import qrcode
from io import BytesIO
from django.db import models
from django.contrib.auth.models import User
from django.core.files.uploadedfile import InMemoryUploadedFile


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
    qrcode = models.ImageField(upload_to='qrcode', blank=True, null=True)

    def generate_qrcode(self):
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=6,
            border=0,
        )
        qr.add_data(str(self.order_id))
        qr.make(fit=True)

        img = qr.make_image()

        buffer = BytesIO()
        img.save(buffer)
        filename = 'order-{}.png'.format(self.order_id)
        file_buffer = InMemoryUploadedFile(buffer, None, filename, 'image/png', buffer.tell(), None)
        self.qrcode.save(filename, file_buffer)

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
