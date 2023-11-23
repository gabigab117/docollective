from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import render, get_object_or_404

from shop.models import Garment
from shop.func.recommendations import recommendations


def index(request):
    # afficher les dernières publications
    count_garment = Garment.objects.filter(activate=True).count()
    if count_garment < 3:
        garments: Garment = Garment.objects.filter(activate=True)
    else:
        # [plus ancien en partant du dernier-3:plus récent][inverser]
        garments: Garment = Garment.objects.filter(activate=True)[count_garment - 3:count_garment:-1]
    return render(request, "shop/index.html", context={"garments": garments})


def all_garments(request):
    garments = Garment.objects.filter(activate=True)

    categories = set((garment.get_category_display(), garment.category) for garment in garments)
    # garments = {garment.category: garment.get_category_display()} categories = garments.keys()

    search = request.GET.get("search")
    if search:
        garments = Garment.objects.filter(
            Q(activate=True),
            Q(description__icontains=search) | Q(color__name__icontains=search)
        )

    redirection = request.GET.get("category")
    if redirection:
        garments = Garment.objects.filter(category=redirection, activate=True)

    return render(request, "shop/all.html", context={"garments": garments, "categories": categories})


@login_required
def recommendations_view(request):
    # Requêtes Q

    user = request.user
    # Haut du corps - ha user.upper_size_property
    upper_garments = recommendations(user, user.upper_size_property, "ha")

    # Bas du corps - pa user.lower_size_property
    lower_garments = recommendations(user, user.lower_size_property, "pa")

    # Pieds - ch user.foot_size_property
    foot_garments = recommendations(user, user.foot_size_property, "ch")

    return render(request, "shop/recommendations.html", context={"upper_garments": upper_garments,
                                                                 "lower_garments": lower_garments,
                                                                 "foot_garments": foot_garments})


def detail_view(request, slug, pk):
    garment: Garment = get_object_or_404(klass=Garment, slug=slug, pk=pk)
    return render(request, "shop/garment.html", context={"garment": garment})