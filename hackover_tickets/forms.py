from django import forms
from . import models as m


class TicketTypeField(forms.ModelChoiceField):

    def label_from_instance(self, obj):
        return "{} - {}".format(obj.name, obj.price)


class TicketForm(forms.Form):
    ticket_type = TicketTypeField(queryset=m.TicketType.objects.filter(public=True))


class MerchandiseField(forms.ModelChoiceField):

    def label_from_instance(self, obj):
        return "{} - {}".format(obj.name, obj.price)


class MerchForm(forms.Form):

    def __init__(self, *args, **kwargs):
        item = kwargs.pop('item')
        super(MerchForm, self).__init__(*args, **kwargs)
        self['amount'].label = '{} - {}'.format(item.name, item.price)

    merchandise = MerchandiseField(queryset=m.Merchandise.objects.all(), widget=forms.HiddenInput())
    amount = forms.IntegerField(initial=0, min_value=0)


class BaseOrderFormSet(forms.BaseFormSet):

    def get_form_kwargs(self, index):
        kwargs = super(BaseOrderFormSet, self).get_form_kwargs(index)
        kwargs['item'] = kwargs['items'][index]
        del kwargs['items']
        return kwargs

MerchOrderFormSet = forms.formset_factory(MerchForm, extra=0, formset=BaseOrderFormSet)
