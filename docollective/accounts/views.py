from django.contrib.auth.views import LoginView
from django.contrib.auth import logout
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
    else:
        form = ExChangerSignupForm()
    return render(request, "accounts/signup.html", context={"form": form})


class ExChangerLogin(LoginView):
    template_name = "accounts/login.html"
    next_page = reverse_lazy("index")


def exchanger_logout(request):
    logout(request)
    return redirect("index")
