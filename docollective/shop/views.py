from django.shortcuts import render, get_object_or_404
from .models import Garment


def index(request):
    # afficher les dernières publications
    count_garment = Garment.objects.filter(purchased=False).count()
    # [plus ancien en partant du dernier-3:plus récent][inverser]
    garments: Garment = Garment.objects.filter(purchased=False)[count_garment-3:count_garment][::-1]
    return render(request, "shop/index.html", context={"garments": garments})


def detail_view(request, slug):
    garment: Garment = get_object_or_404(klass=Garment, slug=slug)
    return render(request, "shop/garment.html", context={"garment": garment})
