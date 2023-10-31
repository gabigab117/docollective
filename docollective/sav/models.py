from django.db import models
from uuid import uuid4
from docollective.settings import AUTH_USER_MODEL


class Ticket(models.Model):
    reference = models.CharField(max_length=36, default=uuid4)
    closed = models.BooleanField(default=False)
    user = models.ForeignKey(AUTH_USER_MODEL, verbose_name="Utilisateur", on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.reference} {self.user} {self.closed}"


class Message(models.Model):
    user = models.ForeignKey(AUTH_USER_MODEL, verbose_name="Utilisateur", on_delete=models.CASCADE)
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE, verbose_name="Ticket")
    subject = models.CharField(max_length=200, verbose_name="Objet")
    message = models.TextField(verbose_name="Message")

    def __str__(self):
        return f"{self.user} {self.ticket}"
