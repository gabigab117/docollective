from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from docollective import settings
from shop.views import index

urlpatterns = [
    path('admin/', admin.site.urls),
    path("", index, name="index"),
    path("account/", include("accounts.urls")),
    path("shop/", include("shop.urls")),
    path("sav/", include("sav.urls")),
    path('verification/', include('verify_email.urls')),
]

if not settings.ENV == "PROD":
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)


admin.site.site_header = 'Docollective'
admin.site.site_title = "Docollective"
