from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout, get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView

from accounts.forms import ExChangerSignupForm
from accounts.models import ExChangerAdresses

from verify_email.email_handler import send_verification_email


def signup(request):
    if request.method == "POST":
        form = ExChangerSignupForm(request.POST)
        if form.is_valid():
            inactive_user = send_verification_email(request, form)
            return redirect("index")
        # Sans le else j'ai un formulaire vide si pas valide
    else:
        form = ExChangerSignupForm()
    return render(request, "accounts/signup.html", context={"form": form})


class ExChangerLogin(LoginView):
    template_name = "accounts/login.html"
    next_page = reverse_lazy("index")


def exchanger_logout(request):
    logout(request)
    return redirect("index")


@login_required
def exchanger_profile(request):
    user = request.user
    try:
        default_adresse = user.adresses.get(user=user, default=True)
    except ObjectDoesNotExist:
        default_adresse = None

    adresses = user.adresses.filter(user=user, default=False)

    return render(request, "accounts/profile.html", context={"user": user,
                                                             "default_adresse": default_adresse,
                                                             "adresses": adresses})


class ProfileUpdate(LoginRequiredMixin, UpdateView):
    model = get_user_model()
    template_name = "accounts/update-profile.html"
    fields = ["upper_size", "lower_size", "foot_size", "favorite_color"]
    success_url = reverse_lazy("accounts:profile")


def default_address_view(request, pk):
    user = request.user

    # current_address = user.adresses.get(user=user, default=True)
    # current_address.default = False
    # current_address.save()
    #
    # new_address = user.adresses.get(pk=pk)
    # new_address.default = True
    # new_address.save()
    # Mettre à jour l'adresse actuelle par défaut
    user.adresses.filter(default=True).update(default=False)

    # Définir la nouvelle adresse comme adresse par défaut
    updated_rows = user.adresses.filter(pk=pk).update(default=True)

    # Vérifier si l'adresse avec `pk=pk` a été mise à jour
    if not updated_rows:
        # Gérer l'erreur ici, par exemple en retournant une réponse d'erreur
        return HttpResponse("Adresse non trouvée", status=404)

    if request.GET.get("redirect") == "validate":
        return redirect("shop:address-choice")

    return redirect("accounts:profile")


class CreateAddress(LoginRequiredMixin, CreateView):
    model = ExChangerAdresses
    template_name = "accounts/create-address.html"
    fields = ["name", "address_1", "address_2", "city", "zip_code", "country"]
    success_url = reverse_lazy("shop:address-choice")

    def form_valid(self, form):
        form.instance.user = self.request.user
        self.request.user.adresses.filter(default=True).update(default=False)
        form.instance.default = True

        return super().form_valid(form)
