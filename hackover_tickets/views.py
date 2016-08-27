from django.shortcuts import render, redirect, reverse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_safe
from . import models as m
from .forms import TicketForm


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
        form = TicketForm
    return render(request, 'tickets/order.html',
                  context={'form': form})


@login_required
@require_safe
def ticket_list(request):
    return render(request, 'tickets/list.html',
                  context={'tickets': m.Ticket.objects.filter(owner=request.user)})
