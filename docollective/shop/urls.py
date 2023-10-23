from django.urls import path
from .views import detail_view, add_to_cart, cart_view, delete_garments, delete_cart, CreateGarment, all_garments, \
    DeleteGarment

app_name = "shop"
urlpatterns = [
    path("garment/<str:slug>/<int:pk>/", detail_view, name="detail"),
    path("add-to-cart/<int:pk>/", add_to_cart, name="add-to-cart"),
    path("cart/", cart_view, name="cart"),
    path("delete-garments/", delete_garments, name="delete-garments"),
    path("delete-cart/", delete_cart, name="delete-cart"),
    path("create-garment/", CreateGarment.as_view(), name="create"),
    path("delete-garment/<int:pk>/", DeleteGarment.as_view(), name="delete-garment"),
    path("all/", all_garments, name="all"),
]
