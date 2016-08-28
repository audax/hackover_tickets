from django.shortcuts import render, redirect, reverse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_safe
from django.db.transaction import atomic
from . import models as m
from .forms import TicketForm, MerchOrderFormSet


@login_required
def index(request):
    return render(request, 'index.html')


@login_required
def ticket_order(request):
    if request.method == 'POST':
        form = TicketForm(request.POST)
        if form.is_valid():
            ticket = m.Ticket.objects.create(type=form.cleaned_data['ticket_type'], owner=request.user)
            return render(request, 'tickets/order_success.html', context={'ticket': ticket})
    else:
        form = TicketForm()
    return render(request, 'tickets/order.html',
                  context={'form': form})


@login_required
@require_safe
def ticket_list(request):
    return render(request, 'tickets/list.html',
                  context={'tickets': m.Ticket.objects.filter(owner=request.user)})


@login_required
def merch_order(request):
    items = m.Merchandise.objects.all()
    if request.method == 'POST':
        formset = MerchOrderFormSet(request.POST, form_kwargs={'items': items})
        if formset.is_valid():
            with atomic():
                order = m.MerchandiseOrder.objects.create(owner=request.user)
                for entry in formset.cleaned_data:
                    m.OrderRelation.objects.create(
                        merchandise=entry['merchandise'],
                        amount=entry['amount'],
                        order=order
                    )
            return render(request, 'merchandise/created.html',
                          context={'order': order}, status=201)
    else:
        formset = MerchOrderFormSet(form_kwargs={'items': items},
                                    initial=[{'merchandise': item} for item in items])
    return render(request, 'merchandise/order.html',
                  context={'form': formset})


@login_required
@require_safe
def merch_list(request):
    return render(request, 'merchandise/list.html',
                  context={'orders': m.MerchandiseOrder.objects.filter(owner=request.user)})
