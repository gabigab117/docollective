from django.urls import path

from .views import new_ticket, pending_tickets, closed_tickets, ticket_view, tickets_admin_view, close_ticket


app_name = "sav"
urlpatterns = [
    path("new-ticket/", new_ticket, name="new-ticket"),
    path("pending-tickets/", pending_tickets, name="pending-tickets"),
    path("closed-tickets/", closed_tickets, name="closed-tickets"),
    path("ticket/<int:pk>", ticket_view, name="ticket"),
    path("tickets-admin/", tickets_admin_view, name="admin-tickets"),
    path("close-ticket/<int:pk>/", close_ticket, name="close"),
]
