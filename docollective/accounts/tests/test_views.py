from django.core.exceptions import ObjectDoesNotExist
from django.test import TestCase, Client
from django.urls import reverse

from accounts.models import ExChanger, ExChangerAdresses


class TestViewShop(TestCase):

    def setUp(self):
        self.client = Client()
        self.user1 = ExChanger.objects.create_user(email="gab@gab.com", username="test_gabigab", first_name="Trouvé",
                                                   last_name="Gabriel", password="12345678")
        self.user2 = ExChanger.objects.create_user(email="gabi@gab.com", username="gabigab2", first_name="Trouvé2",
                                                   last_name="Gabriel2", password="12345678")
        self.superuser1 = ExChanger.objects.create_user(email="super@user.com", username="super", first_name="super",
                                                        last_name="user", password="12345678", is_superuser=True)
        self.address1_user1 = ExChangerAdresses.objects.create(user=self.user1, name="maison",
                                                               address_1="772 route des S", city="OnsenBray",
                                                               zip_code="60650", country="fr", default=True)

    def test_signup_get(self):
        response = self.client.get(reverse("accounts:signup"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "accounts/signup.html")

    def test_signup_post(self):
        data = {
            "username": "Patrick",
            "email": "patrick.trouve5@sfr.fr",
            "first_name": "Patrick",
            "last_name": "Trouvé",
            "type": "nr",
            "password1": "Ringo_Star60456",
            "password2": "Ringo_Star60456"
        }
        response = self.client.post(reverse("accounts:signup"), data=data)
        user = ExChanger.objects.get(username="Patrick")
        self.assertFalse(user.is_active)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("index"))

    def test_signup_post_email_already_exist(self):
        data = {
            "username": "Rob",
            "email": "gab@gab.com",
            "first_name": "Gab",
            "last_name": "Trv",
            "type": "nr",
            "password1": "Ringo_Star60456",
            "password2": "Ringo_Star60456"
        }
        response = self.client.post(reverse("accounts:signup"), data=data)
        self.assertEqual(response.status_code, 200)
        with self.assertRaises(ObjectDoesNotExist):
            ExChanger.objects.get(username="Rob")

    def test_signup_post_username_already_exist(self):
        data = {
            "username": "gabigab2",
            "email": "gab22@gab.com",
            "first_name": "Gab2",
            "last_name": "Trv2",
            "type": "nr",
            "password1": "Ringo_Star60456",
            "password2": "Ringo_Star60456"
        }
        response = self.client.post(reverse("accounts:signup"), data=data)
        self.assertEqual(response.status_code, 200)
        with self.assertRaises(ObjectDoesNotExist):
            ExChanger.objects.get(email="gab22@gab.com")

    def test_login(self):
        response = self.client.post(reverse("accounts:login"), data={"username": "gab@gab.com", "password": "12345678"})
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("index"))

    def test_create_address(self):
        self.client.force_login(self.user1)
        data = {
            "name": "boulot",
            "address_1": "5 rue du pré",
            "city": "Beauvais",
            "zip_code": "60000",
            "country": "fr"
        }
        self.client.post(reverse("accounts:create-address"), data=data)
        address = ExChangerAdresses.objects.get(name="boulot")
        self.assertTrue(address.default)
        self.address1_user1.refresh_from_db()
        self.assertFalse(self.address1_user1.default)
