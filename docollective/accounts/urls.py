from django.urls import path
from .views import signup, ExChangerLogin, exchanger_logout, exchanger_profile, default_address_view, CreateAddress, \
    ExchangerChangePassword, ExchangerPasswordDone, ExchangerResetPassword, ExchangerResetDone, ExchangerResetConfirm, \
    ExchangerResetComplete

app_name = "accounts"
urlpatterns = [
    path('signup/', signup, name="signup"),
    path('login/', ExChangerLogin.as_view(), name="login"),
    path('logout/', exchanger_logout, name="logout"),
    path('profile/', exchanger_profile, name="profile"),
    path('default_adresse/<int:pk>/', default_address_view, name="default_address"),
    path('create-address/', CreateAddress.as_view(), name="create-address"),
    path('change-password/', ExchangerChangePassword.as_view(), name="change-password"),
    path('change-done/', ExchangerPasswordDone.as_view(), name="change-done"),
    path('reset/', ExchangerResetPassword.as_view(), name="reset"),
    path('reset-done/', ExchangerResetDone.as_view(), name="reset-done"),
    path('reset-confirm/<str:uidb64>/<str:token>/', ExchangerResetConfirm.as_view(), name="reset-confirm"),
    path('reset-complete/', ExchangerResetComplete.as_view(), name="reset-complete")
]
