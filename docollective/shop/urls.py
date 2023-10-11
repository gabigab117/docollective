from django.urls import path
from .views import detail_view


app_name = "shop"
urlpatterns = [
    path("garment/<str:slug>/", detail_view, name="detail"),
]
