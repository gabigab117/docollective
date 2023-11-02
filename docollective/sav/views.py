from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.views.decorators.http import require_POST
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect
from django.core.exceptions import PermissionDenied

from .forms import MessageForm, ResponseForm
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


@login_required
def ticket_view(request, pk):
    user = request.user
    ticket = get_object_or_404(Ticket, pk=pk)
    if user != ticket.user and not user.is_superuser:
        raise PermissionDenied()

    ticket_messages = Message.objects.filter(ticket=ticket)

    if request.method == "POST":
        form = ResponseForm(request.POST)
        if form.is_valid():
            form.instance.user = user
            form.instance.ticket = ticket
            form.save()
            return redirect(ticket)
    else:
        form = ResponseForm()
    return render(request, "sav/ticket.html", context={"ticket": ticket,
                                                       "messages": ticket_messages, "form": form})


@user_passes_test(lambda user: user.is_superuser)
def tickets_admin_view(request):
    tickets = Ticket.objects.filter(closed=False)
    return render(request, "sav/tickets-admin.html", context={"tickets": tickets})


@require_POST
def close_ticket(request, pk):
    Ticket.objects.update_or_create(
        pk=pk,
        defaults={"closed": True}
    )
    return redirect("sav:admin-tickets")
