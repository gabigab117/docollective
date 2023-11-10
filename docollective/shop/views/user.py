from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView

from shop.models import Garment, Cart, Order


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