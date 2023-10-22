from django.test import SimpleTestCase
from django.urls import reverse, resolve
from shop.views import index, all_garments, CreateGarment, detail_view, add_to_cart, cart_view, delete_garments, \
    delete_cart


class TestUrls(SimpleTestCase):
    def test_index_url_is_resolved(self):
        url = reverse("index")
        self.assertEquals(resolve(url).func, index)

    def test_all_garments_url_is_resolved(self):
        url = reverse("shop:all")
        self.assertEquals(resolve(url).func, all_garments)

    def test_create_garment_url_is_resolved(self):
        url = reverse("shop:create")
        self.assertEquals(resolve(url).func.view_class, CreateGarment)

    def test_detail_url_is_resolved(self):
        url = reverse("shop:detail", args=['slug', 1])
        self.assertEquals(resolve(url).func, detail_view)

    def test_add_to_cart_url_is_resolved(self):
        url = reverse("shop:add-to-cart", args=[1])
        self.assertEquals(resolve(url).func, add_to_cart)

    def test_cart_view_url_is_resolved(self):
        url = reverse("shop:cart")
        self.assertEquals(resolve(url).func, cart_view)

    def test_delete_garments_url_is_resolved(self):
        url = reverse("shop:delete-garments")
        self.assertEquals(resolve(url).func, delete_garments)

    def test_delete_cart_url_is_resolved(self):
        url = reverse("shop:delete-cart")
        self.assertEquals(resolve(url).func, delete_cart)
