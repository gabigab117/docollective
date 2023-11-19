from django.test import TestCase, Client

from accounts.models import ExChanger
from sav.models import Ticket, Message


class TestModelsSav(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = ExChanger.objects.create_user(email="gab@gab.com", username="test_gabigab", first_name="Trouvé",
                                                   last_name="Gabriel", password="12345678", foot_size=42, type="h")
        self.ticket = Ticket.objects.create(subject="Super Ticket", user=self.user)
        self.message1 = Message.objects.create(user=self.user, ticket=self.ticket, message="coucou")
        self.message2 = Message.objects.create(user=self.user, ticket=self.ticket, message="coucou2")

    def test_message_count_property(self):
        self.assertEqual(self.ticket.messages_count, 2)
