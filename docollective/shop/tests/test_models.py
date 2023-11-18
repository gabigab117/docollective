import os
import shutil
from io import BytesIO

from PIL import Image
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, Client

from accounts.models import ExChanger
from shop.models import Garment, Color


def create_test_image():
    image = Image.new('RGB', (100, 100), color='white')

    image_file = BytesIO()
    image.save(image_file, format="JPEG")
    image_file.seek(0)

    file_name = 'test_image.jpg'
    uploaded_image = SimpleUploadedFile(name=file_name, content=image_file.getvalue(), content_type='image/jpeg')
    return uploaded_image


class TestModels(TestCase):

    def setUp(self):
        self.client = Client()
        self.color1 = Color.objects.create(name="Blanc", hexa="#FFFFFF")
        self.user1 = ExChanger.objects.create_user(email="gab@gab.com", username="test_gabigab", first_name="Trouvé",
                                                   last_name="Gabriel", password="12345678", foot_size=42,
                                                   favorite_color=self.color1, type="h")
        self.garment_1: Garment = Garment.objects.create(description="fringue", user=self.user1, price=10, size=42,
                                                         color=self.color1, type="ho", category="ha",
                                                         activate=True,
                                                         pics_1=create_test_image())

    def tearDown(self):
        folders_path = ["mediafiles/test_gabigab"]
        for path in folders_path:
            if os.path.exists(path):
                shutil.rmtree(path)

    def test_garment_has_a_slug(self):
        self.assertEqual(self.garment_1.slug, "fringue")

    def test_year_property_if_no_year(self):
        self.assertEqual(self.garment_1.garment_year, "NC")
