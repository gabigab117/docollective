from django.db import models
from django.utils import timezone
from docollective.settings import AUTH_USER_MODEL


SIZES = [(str(i), str(i)) for i in range(16, 71)]
YEARS = [(str(y), str(y)) for y in range(1900, timezone.now().year + 1)]
CATEGORY = [("ch", "Chaussures"), ("ma", "Manteaux"), ("pa", "Pantalons"), ("ha", "Hauts"), ("sv", "Sous_vêtements")]
STATE = [("b", "Bon état"), ("tb", "Très bon état"), ("cn", "Comme neuf")]
TYPE = [("h", "Homme"), ("f", "Femme"), ("e", "Enfant")]


def user_directory_path(instance):
    return f"{instance.user.username}"


class Garment(models.Model):
    user = models.ForeignKey(to=AUTH_USER_MODEL, verbose_name="Utilisateur", on_delete=models.CASCADE)
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

    class Meta:
        verbose_name = "Vêtement"


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
