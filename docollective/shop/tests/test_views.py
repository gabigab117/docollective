from django.test import TestCase, Client
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from shop.models import Garment, Order, Cart, Color
from accounts.models import ExChanger

import pathlib
import shutil
from docollective.settings import BASE_DIR

import json


class TestView(TestCase):

    def setUp(self):
        self.client = Client()
        self.index_url = reverse("index")
        self.all_garments_url = reverse("shop:all")
        self.detail_url = reverse("shop:detail", args=["slug", 1])
        self.create_url = reverse("shop:create")

        self.color1 = Color.objects.create(name="Blanc", hexa="#FFFFFF")

        self.user1 = ExChanger.objects.create_user(email="gab@gab.com", username="test_gabigab", first_name="Trouvé",
                                                   last_name="Gabriel", password="12345678")
        self.user2 = ExChanger.objects.create_user(email="gabi@gab.com", username="gabigab2", first_name="Trouvé2",
                                                   last_name="Gabriel2", password="12345678")
        self.garment_1: Garment = Garment.objects.create(description="slug", user=self.user1, price=10,
                                                         color=self.color1, year="1989", type="ho", activate=True,
                                                         pics_1="test/test.jpg")

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
            "pics_1": SimpleUploadedFile(name="test.jpg",
                                         content=open("mediafiles/gabigab117/pant_beige.jpg", "rb").read(),
                                         content_type="image/jpeg")
        })

        self.assertEquals(response.status_code, 302)
        self.assertEquals(Garment.objects.get(description="Chaussette").description, "Chaussette")

        # Nettoyer le dossier Test
        documents = pathlib.Path(BASE_DIR / "mediafiles/test_gabigab")
        shutil.rmtree(documents)

        # Delete View https://youtu.be/hA_VxnxCHbo?si=iVpr_98f3JomVTET 12 minutes
