from django.urls import path
from .views import signup, ExChangerLogin, exchanger_logout, exchanger_profile, default_address_view, CreateAddress

app_name = "accounts"
urlpatterns = [
    path('signup/', signup, name="signup"),
    path('login/', ExChangerLogin.as_view(), name="login"),
    path('logout/', exchanger_logout, name="logout"),
    path('profile/', exchanger_profile, name="profile"),
    path('default_adresse/<int:pk>/', default_address_view, name="default_address"),
    path('create-address/', CreateAddress.as_view(), name="create-address"),
]
