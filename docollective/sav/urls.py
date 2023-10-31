from django.urls import path

from .views import new_ticket, pending_tickets, closed_tickets, ticket_view


app_name = "sav"
urlpatterns = [
    path("new-ticket/", new_ticket, name="new-ticket"),
    path("pending-tickets/", pending_tickets, name="pending-tickets"),
    path("closed-tickets/", closed_tickets, name="closed-tickets"),
    path("ticket/<int:pk>", ticket_view, name="ticket"),
]
