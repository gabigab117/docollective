from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.http import require_POST
from django.forms import modelformset_factory
from .models import Garment, Cart, Order


def index(request):
    # afficher les dernières publications
    count_garment = Garment.objects.filter(purchased=False).count()
    # [plus ancien en partant du dernier-3:plus récent][inverser]
    garments: Garment = Garment.objects.filter(purchased=False)[count_garment-3:count_garment:-1]
    return render(request, "shop/index.html", context={"garments": garments})


def detail_view(request, slug, pk):
    garment: Garment = get_object_or_404(klass=Garment, slug=slug, pk=pk)
    return render(request, "shop/garment.html", context={"garment": garment})


@require_POST
def add_to_cart(request, pk):
    user = request.user

    garment = get_object_or_404(klass=Garment, pk=pk)
    cart, _ = Cart.objects.get_or_create(user=user)

    # Vérifier d'abord si dans le panier de l'utilisateur avec message
    if cart.orders.filter(garment__id=garment.id).exists():
        messages.add_message(request, messages.WARNING, f"{garment.description} est déjà dans votre panier")
        return redirect(garment)

    # Vérifier sinon si dans un panier tout court avec message (mais différent que le précédent)
    elif Cart.objects.filter(orders__garment__id=garment.id).exists():
        messages.add_message(request, messages.WARNING, f"{garment.description} est déjà dans un panier")
        return redirect(garment)

    # Sinon ajouter au panier
    else:
        order = Order.objects.create(user=user, garment=garment)
        cart.orders.add(order)
        return redirect("shop:cart")


@login_required
def cart_view(request):
    user = request.user

    try:
        orders = user.cart.orders.all()
    except ObjectDoesNotExist:
        orders = None

    return render(request, "shop/cart.html", context={"orders": orders})
