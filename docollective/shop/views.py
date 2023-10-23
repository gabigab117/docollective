from django.contrib import messages
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.decorators.http import require_POST
from django.forms import modelformset_factory
from django.views.generic import CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Garment, Cart, Order
from .forms import OrderForm


def index(request):
    # afficher les dernières publications
    count_garment = Garment.objects.filter(activate=True).count()
    if count_garment < 3:
        garments: Garment = Garment.objects.filter(activate=True)
    else:
        # [plus ancien en partant du dernier-3:plus récent][inverser]
        garments: Garment = Garment.objects.filter(activate=True)[count_garment-3:count_garment:-1]
    return render(request, "shop/index.html", context={"garments": garments})


def all_garments(request):
    garments = Garment.objects.filter(activate=True)

    categories = set([(garment.get_category_display(), garment.category) for garment in garments])

    search = request.GET.get("search")
    if search:
        garments = Garment.objects.filter(Q(description__icontains=search) | Q(color__name__icontains=search))

    redirection = request.GET.get("category")
    if redirection:
        garments = Garment.objects.filter(category=redirection)

    return render(request, "shop/all.html", context={"garments": garments, "categories": categories})


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
        orders = user.cart.orders.filter(ordered=False)
    except ObjectDoesNotExist:
        orders = None

    OrderFormSet = modelformset_factory(Order, form=OrderForm, extra=0)
    formset = OrderFormSet(queryset=orders)

    return render(request, "shop/cart.html", context={"forms": formset})


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
    request.user.cart.delete()
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


def order_history(request):
    user = request.user

    return render(request, "shop/order-history.html")
