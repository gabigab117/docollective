from django.urls import path
from .views import detail_view, add_to_cart, cart_view, delete_garments


app_name = "shop"
urlpatterns = [
    path("garment/<str:slug>/<int:pk>/", detail_view, name="detail"),
    path("add-to-cart/<int:pk>/", add_to_cart, name="add-to-cart"),
    path("cart/", cart_view, name="cart"),
    path("delete-garments/", delete_garments, name="delete-garments")
]
