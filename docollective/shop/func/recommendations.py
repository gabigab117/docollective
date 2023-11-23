from django.db.models import Q

from shop.models import Garment


def recommendations(user, size, category):
    query = Garment.objects.filter(
        Q(size=size), Q(activate=True), Q(type=user.type), Q(category=category),
        Q(description__icontains=user.favorite_color_property) | Q(
            color__name__icontains=user.favorite_color_property)
    )
    return query
