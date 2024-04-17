from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.views.decorators.http import require_POST
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect
from django.core.exceptions import PermissionDenied
from django.db import transaction

from .forms import MessageForm, ResponseForm
from .models import Ticket, Message


@login_required
def new_ticket(request):
    """
      Creates a new ticket and message from a user submission.

      This view handles the creation of a new support ticket. On POST request with valid form data,
      it creates a ticket and an associated message, then redirects to the same page with an
      information message. For GET requests, it displays the message form.

      Args:
      request (HttpRequest): The request object, containing user and form data.

      Returns:
      HttpResponse: Renders the new ticket creation page or redirects after form submission.
      """
    user = request.user

    if request.method == "POST":
        form = MessageForm(request.POST)
        if form.is_valid():
            with transaction.atomic():
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
    """
    Displays and handles responses for a specific support ticket.

    Retrieves the ticket by its primary key (pk). If the user is neither the ticket owner nor a
    superuser, access is denied. On a POST request with valid form data, it adds a response to the
    ticket and redirects to the ticket page. For GET requests, it displays the ticket details and
    response form.

    Args:
    request (HttpRequest): The request object, containing user data and form submissions.
    pk (int): Primary key of the ticket to be viewed.

    Returns:
    HttpResponse: Renders the ticket details page or redirects after a response is submitted.
    """
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


@login_required
@require_POST
def close_ticket(request, pk):
    """
     Closes a specified support ticket.

     Only allows the ticket's owner or a superuser to close the ticket. Retrieves the ticket
     by its primary key (pk) and sets its status to closed. Redirects to the index page after closure.

     Args:
     request (HttpRequest): The request object containing user data.
     pk (int): Primary key of the ticket to be closed.

     Returns:
     HttpResponseRedirect: Redirects to the index page after closing the ticket.
     """
    user = request.user
    ticket = Ticket.objects.get(pk=pk)
    if user != ticket.user and not user.is_superuser:
        raise PermissionDenied()
    ticket.closed = True
    ticket.save()
    return redirect("index")
