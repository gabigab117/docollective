from django.contrib.auth.views import PasswordChangeView, PasswordChangeDoneView, PasswordResetView, \
    PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
from django.urls import reverse_lazy


class ExchangerChangePassword(PasswordChangeView):
    template_name = "password/change-form.html"
    success_url = reverse_lazy("accounts:change-done")


class ExchangerPasswordDone(PasswordChangeDoneView):
    template_name = "password/change-done.html"


class ExchangerResetPassword(PasswordResetView):
    template_name = "password/reset.html"
    success_url = reverse_lazy("accounts:reset-done")
    email_template_name = "password/reset-email.html"


class ExchangerResetDone(PasswordResetDoneView):
    template_name = "password/reset-done.html"


class ExchangerResetConfirm(PasswordResetConfirmView):
    template_name = "password/reset-confirm.html"
    success_url = reverse_lazy("accounts:reset-complete")


class ExchangerResetComplete(PasswordResetCompleteView):
    template_name = "password/reset-complete.html"
