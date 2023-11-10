from django.contrib.auth.decorators import user_passes_test
from django.forms import modelformset_factory
from django.http import HttpResponseRedirect
from django.shortcuts import render

from shop.forms import PendingForm, GarmentPendingForm
from shop.models import Order, Garment


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