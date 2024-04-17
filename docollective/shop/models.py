import uuid

from django.contrib import messages
from django.core.mail import send_mail
from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.utils.text import slugify

from docollective.settings import AUTH_USER_MODEL
from shop.func.confirm_order import confirm_order

SIZES = [(str(i), str(i)) for i in range(16, 71)]
YEARS = [(str(y), str(y)) for y in range(1900, timezone.now().year + 1)]
STATE = [("b", "Bon état"), ("tb", "Très bon état"), ("cn", "Comme neuf")]
TYPE = [("h", "Homme"), ("f", "Femme"), ("e", "Enfant")]
CATEGORY = [("ch", "Chaussures"), ("pa", "Pantalons"), ("ha", "Hauts")]


def user_directory_path(instance, filename):
    return f"{instance.user.username}/{filename}"


class Garment(models.Model):
    description = models.CharField(max_length=50, verbose_name="Description", help_text="50 caractères max")
    reference = models.UUIDField(verbose_name="Référence", blank=True, default=uuid.uuid4, editable=True)
    slug = models.SlugField(blank=True)
    user = models.ForeignKey(to=AUTH_USER_MODEL, verbose_name="Utilisateur", on_delete=models.CASCADE,
                             related_name="garments")
    price = models.IntegerField(verbose_name="Prix d'achat")
    size = models.CharField(verbose_name="Taille", choices=SIZES, max_length=10)
    color = models.ForeignKey(to="Color", on_delete=models.SET_NULL, verbose_name="Couleur", null=True)
    year = models.CharField(verbose_name="Année", choices=YEARS, blank=True, max_length=4)
    category = models.CharField(verbose_name="Catégorie", choices=CATEGORY, max_length=20)
    state = models.CharField(verbose_name="Etat", choices=STATE, max_length=20)
    type = models.CharField(verbose_name="Sexe", choices=TYPE, max_length=10)
    pics_1 = models.ImageField(verbose_name="Photo 1", upload_to=user_directory_path)
    pics_2 = models.ImageField(verbose_name="Photo 2", blank=True, null=True, upload_to=user_directory_path)
    pics_3 = models.ImageField(verbose_name="Photo 3", blank=True, null=True, upload_to=user_directory_path)
    published = models.DateTimeField(verbose_name="Date de publication", auto_now_add=True)
    activate = models.BooleanField(default=False, verbose_name="Activé")
    bought = models.BooleanField(default=False, verbose_name="Acheté")

    class Meta:
        verbose_name = "Vêtement"

    def __str__(self):
        return f"{self.user} - {self.get_category_display()} - {self.description}"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.description)

        if self._state.adding:
            super().save(*args, **kwargs)
            Garment.__send_email()
        else:
            super().save(*args, **kwargs)

    @staticmethod
    def __send_email():
        """
            Sends an email notification about a new announcement.

            This static method sends a predefined email with the subject 'Nouvelle annonce' and a
            message stating 'Nouvelle annonce déposée' to a specified recipient list.

            Note:
            This method is private and intended for internal use within its class.
            """
        send_mail(subject="Nouvelle annonce", message="Nouvelle annonce déposée",
                  recipient_list=["gabrieltrouve5@yahoo.com"], from_email=None)

    def get_absolute_url(self):
        # https://docs.djangoproject.com/fr/4.2/ref/models/instances/#get-absolute-url
        return reverse(viewname="shop:detail", kwargs={"slug": self.slug, "pk": self.pk})

    @property
    def garment_year(self):
        return self.year or "NC"


class Color(models.Model):
    name = models.CharField(verbose_name="Nom", max_length=20)
    hexa = models.CharField(verbose_name="Hex", max_length=7)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.hexa.startswith('#'):
            self.hexa = "#" + self.hexa
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Couleur"


class Order(models.Model):
    user = models.ForeignKey(to=AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="Utilisateur")
    garment = models.ForeignKey(to=Garment, on_delete=models.SET_NULL, null=True, verbose_name="Vêtements")
    reference = models.UUIDField(default=uuid.uuid4, editable=True, verbose_name="Référence")
    ordered = models.BooleanField(default=False, verbose_name="Commandée")
    ordered_date = models.DateTimeField(blank=True, null=True)
    validation = models.BooleanField(default=False, verbose_name="Validation du deal")

    class Meta:
        verbose_name = "Commande"

    def __str__(self):
        return f"{self.user} - {self.garment} - {self.ordered_date}"


class Cart(models.Model):
    user = models.OneToOneField(to=AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="Utilisateur")
    orders = models.ManyToManyField(to=Order, verbose_name="Vêtements")
    creation_date = models.DateTimeField(auto_now_add=True, verbose_name="Date de création")

    class Meta:
        verbose_name = "Panier"

    def __str__(self):
        return f"{self.user} - {self.creation_date}"

    def user_delete_cart(self):
        """
           Deletes all orders in the user's cart and then deletes the cart itself.

           This method first removes all orders associated with the cart and then proceeds to delete
           the cart instance.
           """
        self.orders.all().delete()
        self.delete()

    def validate_cart(self, request, user, address):
        """
            Validates the cart, updates orders and garments status, confirms the order, and notifies the user.

            Executes a series of internal methods to update the status of orders and garments, confirm
            the order with the given address, and send a notification to the user. After these operations,
            the cart is deleted.

            Args:
            request (HttpRequest): The HttpRequest object.
            user (User): The user object associated with the cart.
            address (Address): The address object for the order delivery.
            """
        self._update_orders_status()
        self._update_garment_status()
        self._confirm_order_and_notify_user(request, user, address)
        self.delete()

    def _update_orders_status(self):
        self.orders.all().update(ordered=True, ordered_date=timezone.now())

    def _update_garment_status(self):
        Garment.objects.filter(order__in=self.orders.all()).update(activate=False, bought=True)

    def _confirm_order_and_notify_user(self, request, user, address):
        confirm_order(user, self.orders.all(), address)
        messages.add_message(request, messages.INFO,
                             "Pour chaque vêtement demandé vous devez créer "
                             "une annonce et nous envoyer le vêtement concerné.")
