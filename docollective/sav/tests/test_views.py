from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.messages import get_messages

from accounts.models import ExChanger
from sav.models import Ticket, Message


class TicketsTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.user1 = ExChanger.objects.create_user(email="gab@gab.com", username="test_gabigab", first_name="Trouvé",
                                                   last_name="Gabriel", password="12345678", foot_size=42, type="h")
        self.user2 = ExChanger.objects.create_user(email="gabi@gab.com", username="gabigab2", first_name="Trouvé2",
                                                   last_name="Gabriel2", password="12345678")
        self.superuser1 = ExChanger.objects.create_user(email="super@user.com", username="super", first_name="super",
                                                        last_name="user", password="12345678", is_superuser=True)

        self.ticket1 = Ticket.objects.create(subject="Ticket1", user=self.user1)
        self.ticket1_closed = Ticket.objects.create(subject="ClosedTicket", user=self.user1, closed=True)
        self.ticket2 = Ticket.objects.create(subject="Ticket2", user=self.user2)
        self.ticket2_closed = Ticket.objects.create(subject="Ticket2", user=self.user2, closed=True)
        self.message1 = Message.objects.create(user=self.user1, message="MessageUser1", ticket=self.ticket1)
        self.message1 = Message.objects.create(user=self.user2, message="MessageUser2", ticket=self.ticket2)
        self.message3 = Message.objects.create(user=self.user1, message="MessageUser1_2", ticket=self.ticket1_closed)

    def test_new_ticket_if_login_post(self):
        self.client.login(username="gab@gab.com", password="12345678")
        data = {
            "subject": "Test1",
            "message": "Problème"
        }
        response = self.client.post(reverse("sav:new-ticket"), data=data)
        ticket = Ticket.objects.get(subject="Test1")
        message = Message.objects.get(message="Problème")
        framework_message = list(get_messages(response.wsgi_request))
        self.assertEqual(ticket.subject, "Test1")
        self.assertEqual(message.message, 'Problème')
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("sav:new-ticket"))
        self.assertEqual(str(framework_message[0]),
                         f"Ticket {ticket.reference} ouvert. Vous serez averti par mail lorsqu'une réponse sera donnée")

    def test_new_ticket_if_login_get(self):
        self.client.login(username="gab@gab.com", password="12345678")
        response = self.client.get(reverse("sav:new-ticket"))
        self.assertEqual(response.status_code, 200)

    def test_new_ticket_no_login(self):
        response = self.client.get(reverse("sav:new-ticket"))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, f"{reverse('accounts:login')}?next={reverse('sav:new-ticket')}")

    def test_pending_ticket_login_with_my_ticket(self):
        self.client.login(username="gab@gab.com", password="12345678")
        response = self.client.get(reverse("sav:pending-tickets"))
        self.assertIn(self.ticket1.subject, str(response.content))

    def test_pending_ticket_login_with_another_ticket(self):
        self.client.login(username="gab@gab.com", password="12345678")
        response = self.client.get(reverse("sav:pending-tickets"))
        self.assertNotIn(self.ticket2.subject, str(response.content))

    def test_pending_ticket_no_login(self):
        response = self.client.get(reverse("sav:pending-tickets"))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, f"{reverse('accounts:login')}?next={reverse('sav:pending-tickets')}")

    def test_closed_ticket_with_closed_and_not_closed(self):
        self.client.login(username="gab@gab.com", password="12345678")
        response = self.client.get(reverse("sav:closed-tickets"))
        self.assertIn(self.ticket1_closed.subject, str(response.content))
        self.assertNotIn(self.ticket1.subject, str(response.content))

    def test_closed_ticket_another_ticket_user(self):
        self.client.login(username="gab@gab.com", password="12345678")
        response = self.client.get(reverse("sav:closed-tickets"))
        self.assertNotIn(self.ticket2_closed.subject, str(response.content))

    def test_ticket_view_superuser(self):
        self.client.force_login(self.superuser1)
        response = self.client.get(reverse("sav:ticket", kwargs={"pk": 2}))
        self.assertEqual(response.status_code, 200)

    def test_ticket_view_user(self):
        self.client.force_login(self.user2)
        response = self.client.get(reverse("sav:ticket", kwargs={"pk": 3}))
        self.assertEqual(response.status_code, 200)

    def test_ticket_view_user_but_not_his_ticket(self):
        self.client.force_login(self.user1)
        response = self.client.get(reverse("sav:ticket", kwargs={"pk": 3}))
        self.assertEqual(response.status_code, 403)

    def test_tickets_admin_view_is_superuser(self):
        self.client.force_login(self.superuser1)
        response = self.client.get(reverse("sav:admin-tickets"))
        self.assertEqual(response.status_code, 200)
        self.assertNotIn(self.ticket1_closed.subject, str(response.content))
        self.assertIn(self.ticket1.subject, str(response.content))

    def test_tickets_admin_view_if_user(self):
        self.client.force_login(self.user1)
        response = self.client.get(reverse("sav:admin-tickets"))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, f"{reverse('accounts:login')}?next={reverse('sav:admin-tickets')}")

    def test_tickets_admin_no_user(self):
        response = self.client.get(reverse("sav:admin-tickets"))
        self.assertEqual(response.status_code, 302)

    def test_close_ticket_superuser(self):
        self.client.force_login(self.superuser1)
        response = self.client.post(reverse("sav:close", kwargs={"pk": 3}))
        self.ticket2.refresh_from_db()
        self.assertTrue(self.ticket2.closed)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("index"))

    def test_close_ticket_user(self):
        self.client.force_login(self.user1)
        response = self.client.post(reverse("sav:close", kwargs={"pk": 1}))
        self.ticket1.refresh_from_db()
        self.assertTrue(self.ticket1.closed)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("index"))

    def test_close_ticket_another_user(self):
        self.client.force_login(self.user1)
        response = self.client.post(reverse("sav:close", kwargs={"pk": 3}))
        self.ticket2.refresh_from_db()
        self.assertFalse(self.ticket2.closed)
        self.assertEqual(response.status_code, 403)

    def test_close_ticket_not_logged_in(self):
        response = self.client.post(reverse("sav:close", kwargs={"pk": 3}))
        self.assertEqual(response.status_code, 302)
        self.ticket2.refresh_from_db()
        self.assertFalse(self.ticket2.closed)
        self.assertRedirects(response, f"{reverse('accounts:login')}?next={reverse('sav:close', kwargs={'pk': 3})}")
