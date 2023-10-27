from django.test import TestCase, Client
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.exceptions import ObjectDoesNotExist
from shop.models import Garment, Order, Cart, Color
from accounts.models import ExChanger

import os
import shutil
from PIL import Image
from io import BytesIO

import json


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
        self.detail_url = reverse("shop:detail", args=["fringue", 1])
        self.create_url = reverse("shop:create")
        self.delete_url = reverse("shop:delete-garment", args=[1])

        self.color1 = Color.objects.create(name="Blanc", hexa="#FFFFFF")

        self.user1 = ExChanger.objects.create_user(email="gab@gab.com", username="test_gabigab", first_name="Trouvé",
                                                   last_name="Gabriel", password="12345678")
        self.user2 = ExChanger.objects.create_user(email="gabi@gab.com", username="gabigab2", first_name="Trouvé2",
                                                   last_name="Gabriel2", password="12345678")
        self.garment_1: Garment = Garment.objects.create(description="fringue", user=self.user1, price=10, size=42,
                                                         color=self.color1, year="1989", type="ho", category="ch",
                                                         activate=True,
                                                         pics_1=create_test_image())

    def tearDown(self):
        folder_path = "mediafiles/test_gabigab"
        if os.path.exists(folder_path):
            shutil.rmtree(folder_path)

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

    def test_create_garment_POST_no_login(self):
        response = self.client.get(self.create_url)
        self.assertEquals(response.status_code, 302)
        self.assertRedirects(response, f"{reverse('accounts:login')}?next={reverse('shop:create')}")

    def test_delete_garment(self):
        response = self.client.delete(self.delete_url, {"pk": 1})
        self.assertEquals(Garment.objects.filter(pk=1).first(), None)
        self.assertEquals(response.status_code, 302)
