from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.forms import modelformset_factory
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from shop.forms import OrderForm
from shop.models import Garment, Order


@require_POST
@login_required
def add_to_cart(request, pk):
    user = request.user
    garment = get_object_or_404(klass=Garment, pk=pk)
    action = user.add_to_cart(request=request, garment=garment)
    return redirect("shop:cart") if action else redirect(garment)


@login_required
def cart_view(request):
    user = request.user

    try:
        orders = user.cart.orders.filter(ordered=False)
    except ObjectDoesNotExist:
        orders = None

    OrderFormSet = modelformset_factory(Order, form=OrderForm, extra=0)
    formset = OrderFormSet(queryset=orders)

    return render(request, "shop/cart.html", context={"forms": formset})


@login_required
def address_choice_view(request):
    user = request.user
    try:
        default_adresse = user.adresses.get(user=user, default=True)
    except ObjectDoesNotExist:
        default_adresse = None
    adresses = user.adresses.filter(user=user, default=False)

    return render(request, "shop/address-choice.html", context={"user": user,
                                                                "default_adresse": default_adresse,
                                                                "adresses": adresses})


@require_POST
@login_required
def validate_cart_view(request):
    user = request.user
    address = user.adresses.get(default=True)
    cart = user.cart

    cart.validate_cart(user, address)

    messages.add_message(request, messages.INFO,
                         "Pour chaque vêtement demandé vous devez créer "
                         "une annonce et nous envoyer le vêtement concerné.")
    return redirect("shop:my-shop")


@login_required
@require_POST
def delete_garments_cart(request):
    user = request.user
    OrderFormSet = modelformset_factory(Order, form=OrderForm, extra=0)
    formset = OrderFormSet(request.POST, queryset=user.cart.orders.filter(ordered=False))

    if formset.is_valid():
        formset.save()
    return redirect("shop:cart")


@login_required
@require_POST
def delete_cart(request):
    request.user.cart.user_delete_cart()
    return redirect("index")
