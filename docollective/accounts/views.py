from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.contrib.auth import logout
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy

from .forms import ExChangerSignupForm

from verify_email.email_handler import send_verification_email


def signup(request):
    if request.method == "POST":
        form = ExChangerSignupForm(request.POST)
        if form.is_valid():
            inactive_user = send_verification_email(request, form)
            return redirect("index")
        # Sans le else j'a iun formulaire vide si pas valide
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
    default_adresse = user.adresses.get(user=user, default=True)
    adresses = user.adresses.filter(user=user, default=False)

    return render(request, "accounts/profile.html", context={"user": user,
                                                             "default_adresse": default_adresse,
                                                             "adresses": adresses})


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

    return redirect("accounts:profile")
