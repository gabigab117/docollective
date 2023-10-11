from django.shortcuts import render, get_object_or_404
from .models import Garment


def index(request):
    # afficher les dernières publications
    garments: Garment = Garment.objects.filter(purchased=False).order_by("-published")
    return render(request, "shop/index.html", context={"garments": garments})


def detail_view(request, slug):
    garment: Garment = get_object_or_404(klass=Garment, slug=slug)
    return render(request, "shop/garment.html", context={"garment": garment})
