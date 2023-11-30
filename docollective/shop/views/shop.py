from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import render, get_object_or_404

from shop.models import Garment


def index(request):
    """
       Displays the index page with the latest garment publications.

       Fetches and displays either all activated garments if their count is less than 3,
       or the last three activated garments in reverse order (newest first). Renders the
       index page of the shop with the selected garments.

       Args:
       request (HttpRequest): The request object.

       Returns:
       HttpResponse: Renders the shop's index page with the context of selected garments.
       """
    count_garment = Garment.objects.filter(activate=True).count()
    if count_garment < 3:
        garments: Garment = Garment.objects.filter(activate=True)
    else:
        garments: Garment = Garment.objects.filter(activate=True)[count_garment - 3:count_garment:-1]
    return render(request, "shop/index.html", context={"garments": garments})


def all_garments(request):
    """
      Displays all active garments, with optional filtering by search query or category.

      Fetches all garments that are marked as active. Allows filtering based on a search
      query (matching in garment descriptions or colors) or a selected category. It also
      prepares a set of categories for display and filtering purposes.

      Args:
      request (HttpRequest): The request object containing potential search and category filters.

      Returns:
      HttpResponse: Renders the page showing all or filtered garments along with available categories.
      """
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
    """
        Displays personalized garment recommendations for the logged-in user.

        This view generates recommendations for upper body, lower body, and footwear based on
        the user's preferences and sizes. It utilizes the 'recommendations' method of the user
        to fetch suitable garments in each category.

        Args:
        request (HttpRequest): The request object containing the user's information.

        Returns:
        HttpResponse: Renders the recommendations page with garments for each body part category.
        """
    user = request.user

    upper_garments = user.recommendations(user.upper_size_property, "ha")

    lower_garments = user.recommendations(user.lower_size_property, "pa")

    foot_garments = user.recommendations(user.foot_size_property, "ch")

    return render(request, "shop/recommendations.html", context={"upper_garments": upper_garments,
                                                                 "lower_garments": lower_garments,
                                                                 "foot_garments": foot_garments})


def detail_view(request, slug, pk):
    garment: Garment = get_object_or_404(klass=Garment, slug=slug, pk=pk)
    return render(request, "shop/garment.html", context={"garment": garment})