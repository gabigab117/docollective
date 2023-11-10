from django.urls import path
from .views import detail_view, add_to_cart, cart_view, delete_garments_cart, delete_cart, CreateGarment, all_garments, \
    DeleteGarment, my_shop_view, validate_cart, address_choice_view, admin_deal_validation_view, recommendations_view, \
    admin_advert_validation_view

app_name = "shop"
urlpatterns = [
    path("garment/<str:slug>/<int:pk>/", detail_view, name="detail"),
    path("add-to-cart/<int:pk>/", add_to_cart, name="add-to-cart"),
    path("cart/", cart_view, name="cart"),
    path("address-choice/", address_choice_view, name="address-choice"),
    path("validate-cart/", validate_cart, name="validate-cart"),
    path("delete-garments/", delete_garments_cart, name="delete-garments"),
    path("delete-cart/", delete_cart, name="delete-cart"),
    path("create-garment/", CreateGarment.as_view(), name="create"),
    path("delete-garment/<int:pk>/", DeleteGarment.as_view(), name="delete-garment"),
    path("all/", all_garments, name="all"),
    path("recommendations/", recommendations_view, name="recommendations"),
    path("my-shop/", my_shop_view, name="my-shop"),
    path("admin-validation/", admin_deal_validation_view, name="admin-validation"),
    path("admin-ad-validation/", admin_advert_validation_view, name="admin-advert"),
]
