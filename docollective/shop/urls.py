from django.urls import path
from .views import detail_view, add_to_cart, cart_view


app_name = "shop"
urlpatterns = [
    path("garment/<str:slug>/", detail_view, name="detail"),
    path("add-to-cart/<str:slug>/", add_to_cart, name="add-to-cart"),
    path("cart/", cart_view, name="cart")
]
