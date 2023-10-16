import uuid
from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.utils.text import slugify

from docollective.settings import AUTH_USER_MODEL

SIZES = [(str(i), str(i)) for i in range(16, 71)]
YEARS = [(str(y), str(y)) for y in range(1900, timezone.now().year + 1)]
CATEGORY = [("ch", "Chaussures"), ("ma", "Manteaux"), ("pa", "Pantalons"), ("ha", "Hauts"), ("sv", "Sous_vêtements")]
STATE = [("b", "Bon état"), ("tb", "Très bon état"), ("cn", "Comme neuf")]
TYPE = [("h", "Homme"), ("f", "Femme"), ("e", "Enfant")]


def user_directory_path(instance, filename):
    return f"{instance.user.username}/{filename}"


class Garment(models.Model):
    description = models.CharField(max_length=50, verbose_name="Description")
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
    purchased = models.BooleanField(default=False, verbose_name="Acheté")
    buyer = models.ForeignKey(to=AUTH_USER_MODEL, verbose_name="Acheteur", on_delete=models.CASCADE, null=True,
                              blank=True)
    published = models.DateTimeField(verbose_name="Date de publication", auto_now_add=True)

    class Meta:
        verbose_name = "Vêtement"

    def __str__(self):
        return f"{self.user} - {self.get_category_display()} - {self.description}"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.description)
        super().save(*args, **kwargs)

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
        return f"{self.name} - {self.hexa}"

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
    ordered = models.BooleanField(default=False, verbose_name="Acquitté")
    ordered_date = models.DateTimeField(blank=True, null=True)

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

    def delete(self, *args, **kwargs):
        for order in self.orders.all():
            order.delete()
        super().delete(*args, **kwargs)
