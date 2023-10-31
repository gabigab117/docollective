from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.core.exceptions import PermissionDenied

from .forms import MessageForm
from .models import Ticket, Message


@login_required
def new_ticket(request):
    user = request.user

    if request.method == "POST":
        form = MessageForm(request.POST)
        if form.is_valid():
            ticket = Ticket.objects.create(user=user, subject=form.cleaned_data["subject"])
            form.instance.user = user
            form.instance.ticket = ticket
            form.save()
            messages.add_message(request,
                                 message=f"Ticket {ticket.reference} ouvert. "
                                         f"Vous serez averti par mail lorsqu'une réponse sera donnée",
                                 level=messages.INFO)
            return HttpResponseRedirect(request.path)
    else:
        form = MessageForm()
    return render(request, "sav/new-ticket.html", context={"form": form})


@login_required
def pending_tickets(request):
    user = request.user
    tickets = Ticket.objects.filter(user=user, closed=False)

    return render(request, "sav/pending-tickets.html", context={"tickets": tickets})


@login_required
def closed_tickets(request):
    user = request.user
    tickets = Ticket.objects.filter(user=user, closed=True)

    return render(request, "sav/closed-tickets.html", context={"tickets": tickets})


def ticket_view(request, pk):
    ticket = get_object_or_404(Ticket, pk=pk)
    if request.user != ticket.user:
        raise PermissionDenied()
    ticket_messages = Message.objects.filter(ticket=ticket)
    return render(request, "sav/ticket.html", context={"ticket": ticket, "messages": ticket_messages})
