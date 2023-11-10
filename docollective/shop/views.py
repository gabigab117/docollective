from django.contrib import messages
from django.db.models import Q
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.decorators.http import require_POST
from django.forms import modelformset_factory
from django.views.generic import CreateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils import timezone
from .models import Garment, Cart, Order
from .forms import OrderForm, PendingForm, GarmentPendingForm

from .emails.confirm_order import confirm_order


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
    user = request.user
    # Haut du corps
    upper_garments = Garment.objects.filter(
        Q(size=user.upper_size_property), Q(activate=True), Q(type=user.type), Q(category="ha"),
        Q(description__icontains=user.favorite_color_property) | Q(
            color__name__icontains=user.favorite_color_property)
    )
    # Bas du corps
    lower_garments = Garment.objects.filter(
        Q(size=user.lower_size_property), Q(activate=True), Q(type=user.type), Q(category="pa"),
        Q(description__icontains=user.favorite_color_property) | Q(
            color__name__icontains=user.favorite_color_property)
    )
    # Pieds
    foot_garments = Garment.objects.filter(
        Q(size=user.foot_size_property), Q(activate=True), Q(type=user.type), Q(category="ch"),
        Q(description__icontains=user.favorite_color_property) | Q(
            color__name__icontains=user.favorite_color_property)
    )
    return render(request, "shop/recommendations.html", context={"upper_garments": upper_garments,
                                                                 "lower_garments": lower_garments,
                                                                 "foot_garments": foot_garments})


def detail_view(request, slug, pk):
    garment: Garment = get_object_or_404(klass=Garment, slug=slug, pk=pk)
    return render(request, "shop/garment.html", context={"garment": garment})


@require_POST
@login_required
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
def validate_cart(request):
    user = request.user
    address = user.adresses.get(default=True)
    cart = user.cart
    orders = cart.orders.all()
    orders.all().update(ordered=True, ordered_date=timezone.now())
    for order in orders:
        order.garment.activate = False
        order.garment.bought = True
        order.garment.save()

    cart.delete()
    confirm_order(user=user, orders=orders, address=address)
    messages.add_message(request, messages.INFO,
                         "Pour chaque vêtement demandé vous devez créer "
                         "une annonce et nous envoyer le vêtement de l'annonce.")
    return redirect("shop:my-shop")


@require_POST
def delete_garments(request):
    user = request.user
    OrderFormSet = modelformset_factory(Order, form=OrderForm, extra=0)
    formset = OrderFormSet(request.POST, queryset=user.cart.orders.filter(ordered=False))

    if formset.is_valid():
        formset.save()
    return redirect("shop:cart")


@require_POST
def delete_cart(request):
    request.user.cart.user_delete_cart()
    return redirect("index")


class CreateGarment(LoginRequiredMixin, CreateView):
    model = Garment
    template_name = "shop/create-garment.html"
    success_url = reverse_lazy("index")
    fields = ["description", "price", "size", "color", "year", "category", "state", "type", "pics_1",
              "pics_2", "pics_3"]

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class DeleteGarment(LoginRequiredMixin, DeleteView):
    model = Garment
    success_url = reverse_lazy("index")
    template_name = "shop/delete-garment.html"

    def form_valid(self, form):
        garment = self.get_object()
        if Cart.objects.filter(orders__garment__id=garment.id).exists():
            messages.add_message(self.request, messages.WARNING,
                                 "L'annonce est dans le panier d'un utilisateur, impossible de la supprimer.")
            return redirect(garment)
        return super().form_valid(form)


@login_required
def my_shop_view(request):
    user = request.user
    # Penser à la recherche dans les commandes

    # Mes annonces
    ads_published = Garment.objects.filter(user=user, activate=True)

    # En modération
    ads_not_published = Garment.objects.filter(user=user, activate=False)

    # Acheté
    purchases = Order.objects.filter(user=user, validation=True)

    # Achats en attente de validation de la plateforme
    purchases_not_validate = Order.objects.filter(user=user, validation=False)

    return render(request, "shop/my_shop.html", context={
        "ads_published": ads_published,
        "ads_not_published": ads_not_published,
        "purchases": purchases,
        "purchases_not_validate": purchases_not_validate,
    })


# Validation des échanges par les admin
@user_passes_test(lambda user: user.is_superuser)
def admin_deal_validation_view(request):
    pending_orders = Order.objects.filter(validation=False, ordered=True)
    PendingFormSet = modelformset_factory(Order, PendingForm, extra=0)
    formset = PendingFormSet(queryset=pending_orders)

    if request.method == "POST":
        formset = PendingFormSet(request.POST, queryset=pending_orders)
        if formset.is_valid():
            formset.save()
            return HttpResponseRedirect(request.path)
    return render(request, "shop/admin-validation.html", context={"forms": formset})


# Validation des annonces
@user_passes_test(lambda user: user.is_superuser)
def admin_advert_validation_view(request):
    pending_garment = Garment.objects.filter(activate=False, bought=False)
    GarmentPendingFormSet = modelformset_factory(Garment, GarmentPendingForm, extra=0)
    formset = GarmentPendingFormSet(queryset=pending_garment)

    if request.method == "POST":
        formset = GarmentPendingFormSet(request.POST, queryset=pending_garment)
        if formset.is_valid():
            formset.save()
            return HttpResponseRedirect(request.path)

    return render(request, "shop/admin-ad-validation.html", context={"forms": formset})
