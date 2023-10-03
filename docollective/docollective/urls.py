from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path

from docollective import settings
from shop.views import index

urlpatterns = [
    path('admin/', admin.site.urls),
    path("", index, name="index"),
]


urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)


admin.site.site_header = 'Docollective'
admin.site.site_title = "Docollective"
