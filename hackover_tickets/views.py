from django.shortcuts import render, get_object_or_404
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


@login_required
@require_safe
def ticket_show(request, order_id):
    ticket = get_object_or_404(m.Ticket, order_id=order_id)
    if not ticket.paid:
        return render(request, 'tickets/not_paid.html',
                      status=403, context={'ticket': ticket})
    ticket.accessed = True
    try:
        url = ticket.qrcode.url
    except ValueError:
        ticket.generate_qrcode()
        url = ticket.qrcode.url
    ticket.save()
    return render(request, 'tickets/show.html',
                  context={'ticket': ticket, 'qrcode_url': url})


@login_required
@require_safe
def merch_show(request, order_id):
    order = get_object_or_404(m.MerchandiseOrder, order_id=order_id)
    if not order.paid:
        return render(request, 'merchandise/not_paid.html',
                      status=403, context={'order': order})
    order.accessed = True
    try:
        url = order.qrcode.url
    except ValueError:
        order.generate_qrcode()
        url = order.qrcode.url
    order.save()
    return render(request, 'merchandise/show.html',
                  context={'order': order, 'qrcode_url': url})
