from django.test import TestCase, Client
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone

from shop.models import Garment, Order, Cart, Color
from accounts.models import ExChanger

import os
import shutil
from PIL import Image
from io import BytesIO


def create_test_image():
    image = Image.new('RGB', (100, 100), color='white')

    image_file = BytesIO()
    image.save(image_file, format="JPEG")
    image_file.seek(0)

    file_name = 'test_image.jpg'
    uploaded_image = SimpleUploadedFile(name=file_name, content=image_file.getvalue(), content_type='image/jpeg')
    return uploaded_image


class TestView(TestCase):

    def setUp(self):
        self.client = Client()
        self.index_url = reverse("index")
        self.all_garments_url = reverse("shop:all")
        self.detail_url = reverse("shop:detail", kwargs={"slug": "fringue", "pk": 1})
        self.create_url = reverse("shop:create")
        self.delete_url = reverse("shop:delete-garment", kwargs={"pk": 1})

        self.color1 = Color.objects.create(name="Blanc", hexa="#FFFFFF")

        self.user1 = ExChanger.objects.create_user(email="gab@gab.com", username="test_gabigab", first_name="Trouvé",
                                                   last_name="Gabriel", password="12345678")
        self.user2 = ExChanger.objects.create_user(email="gabi@gab.com", username="gabigab2", first_name="Trouvé2",
                                                   last_name="Gabriel2", password="12345678")
        self.garment_1: Garment = Garment.objects.create(description="fringue", user=self.user1, price=10, size=42,
                                                         color=self.color1, year="1989", type="ho", category="ch",
                                                         activate=True,
                                                         pics_1=create_test_image())
        self.garment_2: Garment = Garment.objects.create(description="habit", user=self.user2, price=10, size=42,
                                                         color=self.color1, year="1999", type="ho", category="ch",
                                                         activate=True,
                                                         pics_1=create_test_image())
        self.garment_to_order_user1: Garment = Garment.objects.create(description="chaussures", user=self.user2,
                                                                      price=10,
                                                                      size=42,
                                                                      color=self.color1, year="1999", type="ho",
                                                                      category="ch",
                                                                      activate=True,
                                                                      pics_1=create_test_image())
        self.garment_to_order_user2: Garment = Garment.objects.create(description="jean", user=self.user1,
                                                                      price=10,
                                                                      size=42,
                                                                      color=self.color1, year="1999", type="ho",
                                                                      category="ch",
                                                                      activate=True,
                                                                      pics_1=create_test_image())
        self.order_user1: Order = Order.objects.create(user=self.user1, garment=self.garment_to_order_user1,
                                                       ordered=True, ordered_date=timezone.now())
        self.order_user2: Order = Order.objects.create(user=self.user2, garment=self.garment_to_order_user2,
                                                       ordered=True, ordered_date=timezone.now())

    def tearDown(self):
        folders_path = ["mediafiles/test_gabigab", "mediafiles/gabigab2"]
        for path in folders_path:
            if os.path.exists(path):
                shutil.rmtree(path)

    def test_index_GET(self):
        response = self.client.get(self.index_url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, "shop/index.html")

    def test_all_garments_GET(self):
        response = self.client.get(self.all_garments_url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, "shop/all.html")

    def test_detail_GET(self):
        response = self.client.get(self.detail_url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed("shop/garment.html")

    def test_create_garment_POST(self):
        self.client.login(username="gab@gab.com", password="12345678")

        response = self.client.post(self.create_url, {
            "description": "Chaussette",
            "user": self.user1,
            "price": 10,
            "size": 42,
            "color": self.color1.id,
            "year": "1989",
            "category": "ch",
            "state": "b",
            "type": "h",
            "pics_1": create_test_image()
        })

        self.assertEquals(response.status_code, 302)
        self.assertRedirects(response, reverse("index"))
        self.assertEquals(Garment.objects.get(description="Chaussette").description, "Chaussette")
        self.assertTemplateUsed("shop/create-garment.html")

    def test_create_garment_POST_no_login(self):
        response = self.client.get(self.create_url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, f"{reverse('accounts:login')}?next={reverse('shop:create')}")

    def test_delete_garment(self):
        self.client.login(username="gab@gab.com", password="12345678")
        response = self.client.delete(self.delete_url, {"pk": 1})
        with self.assertRaises(ObjectDoesNotExist):
            Garment.objects.get(pk=1)
        self.assertEqual(response.status_code, 302)
        self.assertTemplateUsed("shop/delete-garment.html")

    def test_delete_garment_no_login(self):
        response = self.client.delete(self.delete_url, data={"pk": 1})
        garment = Garment.objects.get(pk=1)
        self.assertEqual(garment.slug, "fringue")
        self.assertEqual(response.status_code, 302)
        expected_url = f"{reverse('accounts:login')}?next={reverse('shop:delete-garment', kwargs={'pk': 1})}"
        self.assertRedirects(response, expected_url)

    def test_my_shop_login(self):
        self.client.login(username="gab@gab.com", password="12345678")
        response = self.client.get(reverse("shop:my-shop"))
        self.assertTemplateUsed("shop/my-shop.html")
        self.assertEqual(response.status_code, 200)
        self.assertIn(self.garment_1.description, str(response.content))
        self.assertIn(str(self.order_user1.reference), str(response.content))

    def test_my_shop_no_login(self):
        response = self.client.get(reverse("shop:my-shop"))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, f"{reverse('accounts:login')}?next={reverse('shop:my-shop')}")

    def test_my_shop_login_display_another_user_garment_and_order(self):
        """
        Tableau de bord utilisateur, on ne doit pas afficher les annonces d'un autre
        utilisateur.
        """
        self.client.login(username="gab@gab.com", password="12345678")
        response = self.client.get(reverse("shop:my-shop"))
        # L'annonce ci-dessous appartient à self.user2
        self.assertNotIn(self.garment_2.description, str(response.content))
        self.assertNotIn(str(self.order_user2.reference), str(response.content))
