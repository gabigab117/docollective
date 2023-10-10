from django.shortcuts import render
from .models import Garment


def index(request):
    # afficher les dernières publications
    garments: Garment = Garment.objects.filter(purchased=False).order_by("-published")
    return render(request, "shop/index.html", context={"garments": garments})
