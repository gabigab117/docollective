from django.db import models
from uuid import uuid4

from django.urls import reverse

from docollective.settings import AUTH_USER_MODEL


class Ticket(models.Model):
    reference = models.CharField(max_length=36, default=uuid4)
    subject = models.CharField(max_length=200, verbose_name="Objet")
    closed = models.BooleanField(default=False)
    user = models.ForeignKey(AUTH_USER_MODEL, verbose_name="Utilisateur", on_delete=models.CASCADE)
    date = models.DateTimeField(verbose_name="Publication", auto_now_add=True)

    def __str__(self):
        return f"{self.date} {self.subject} {self.closed}"

    def get_absolute_url(self):
        return reverse(viewname="sav:ticket", kwargs={"pk": self.pk})

    @property
    def messages_count(self):
        return Message.objects.filter(ticket=self).count()


class Message(models.Model):
    user = models.ForeignKey(AUTH_USER_MODEL, verbose_name="Utilisateur", on_delete=models.CASCADE)
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE, verbose_name="Ticket")
    message = models.TextField(verbose_name="Message")
    date = models.DateTimeField(verbose_name="Publication", auto_now_add=True)

    def __str__(self):
        return f"{self.user} {self.ticket} {self.date}"
