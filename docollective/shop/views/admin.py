from django.contrib.auth.decorators import user_passes_test
from django.forms import modelformset_factory
from django.http import HttpResponseRedirect
from django.shortcuts import render

from shop.forms import PendingForm, GarmentPendingForm
from shop.models import Order, Garment


@user_passes_test(lambda user: user.is_superuser)
def admin_deal_validation_view(request):
    """
       Handles the validation of pending orders by an admin.

       Displays a formset for all orders that are marked as ordered but not yet validated.
       On POST, it updates the status of these orders based on the admin's input and then
       reloads the page. This view is restricted to superuser access only.

       Args:
       request (HttpRequest): The request object containing form data for POST requests.

       Returns:
       HttpResponse: Renders the admin validation page with the formset for pending orders.
       """
    pending_orders = Order.objects.filter(validation=False, ordered=True)
    PendingFormSet = modelformset_factory(Order, PendingForm, extra=0)
    formset = PendingFormSet(queryset=pending_orders)

    if request.method == "POST":
        formset = PendingFormSet(request.POST, queryset=pending_orders)
        if formset.is_valid():
            formset.save()
            return HttpResponseRedirect(request.path)
    return render(request, "shop/admin-validation.html", context={"forms": formset})


@user_passes_test(lambda user: user.is_superuser)
def admin_advert_validation_view(request):
    """
        Manages the validation of pending garment advertisements by an admin.

        This view displays a formset for all garments that are not activated and not bought.
        On a POST request, it processes the submitted formset to update the status of these garments
        based on the admin's decisions and then refreshes the page. Access to this view is restricted
        to superusers only.

        Args:
        request (HttpRequest): The request object, containing form data for POST requests.

        Returns:
        HttpResponse: Renders the admin advertisement validation page with the formset for pending garments.
        """
    pending_garment = Garment.objects.filter(activate=False, bought=False)
    GarmentPendingFormSet = modelformset_factory(Garment, GarmentPendingForm, extra=0)
    formset = GarmentPendingFormSet(queryset=pending_garment)

    if request.method == "POST":
        formset = GarmentPendingFormSet(request.POST, queryset=pending_garment)
        if formset.is_valid():
            formset.save()
            return HttpResponseRedirect(request.path)

    return render(request, "shop/admin-ad-validation.html", context={"forms": formset})
