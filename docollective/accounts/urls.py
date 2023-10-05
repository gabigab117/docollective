from django.urls import path
from .views import signup, ExChangerLogin, exchanger_logout, exchanger_profile


app_name = "accounts"
urlpatterns = [
    path('signup/', signup, name="signup"),
    path('login/', ExChangerLogin.as_view(), name="login"),
    path('logout/', exchanger_logout, name="logout"),
    path('profile/', exchanger_profile, name="profile"),
]
