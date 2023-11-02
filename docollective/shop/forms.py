from django import forms
from .models import Order, Garment


class OrderForm(forms.ModelForm):
    delete = forms.BooleanField(initial=False, label="Supprimer", required=False)

    class Meta:
        model = Order
        fields = ["delete"]

    def save(self, *args, **kwargs):
        if self.cleaned_data["delete"]:
            self.instance.delete()

            if self.instance.user.cart.orders.count() == 0:
                # Instance est Order
                self.instance.user.cart.delete()
                # On retourne True pour éviter de save
            return True

        return super().save(*args, **kwargs)


class PendingForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ["validation"]


class GarmentPendingForm(forms.ModelForm):
    class Meta:
        model = Garment
        fields = ["activate"]
