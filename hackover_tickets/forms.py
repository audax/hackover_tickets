from django import forms
from . import models as m


class TicketTypeField(forms.ModelChoiceField):

    def label_from_instance(self, obj):
        return "{} - {}".format(obj.name, obj.price)


class TicketForm(forms.Form):
    ticket_type = TicketTypeField(queryset=m.TicketType.objects.filter(public=True))


class MerchForm(forms.Form):

    name = forms.CharField(disabled=False)
    price = forms.DecimalField(disabled=False)
    amount = forms.IntegerField(initial=0)


MerchOrderFormSet = forms.formset_factory(MerchForm)
