import iso3166
from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager


class ExChangerManager(BaseUserManager):
    def create_user(self, email, username, first_name, last_name, password, **kwargs):
        if not email:
            raise ValueError("email obligatoire")
        user = self.model(email=self.normalize_email(email), username=username, first_name=first_name,
                          last_name=last_name, **kwargs)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, username, first_name, last_name, password, **kwargs):
        user = self.create_user(email, username, first_name, last_name, password, **kwargs)
        user.is_staff = True
        user.is_superuser = True
        user.is_active = True
        user.save()
        return user


class ExChanger(AbstractUser):
    email = models.EmailField(unique=True)

    REQUIRED_FIELDS = ["username", "first_name", "last_name"]
    USERNAME_FIELD = "email"

    objects = ExChangerManager()

    # Règle : 5 adresses maximum par utilisateur
    @property
    def number_adresses(self):
        number_adresses = ExChangerAdresses.objects.filter(user=self).count()
        return number_adresses


class ExChangerAdresses(models.Model):
    user: ExChanger = models.ForeignKey(to=ExChanger, on_delete=models.CASCADE, verbose_name="Utilisateur",
                                        related_name="adresses")
    name = models.CharField(max_length=200, verbose_name="Nom de l'adresse")
    address_1 = models.CharField(max_length=1024, help_text="Voirie, numéro de rue", verbose_name="Adresse 1")
    address_2 = models.CharField(max_length=1024, help_text="Bât, étage, lieu-dit", verbose_name="Adresse 2",
                                 blank=True)
    city = models.CharField(max_length=1024, verbose_name="Commune")
    zip_code = models.CharField(max_length=32, verbose_name="Code Postal")
    country = models.CharField(max_length=2, choices=[(c.alpha2.lower(), c.name) for c in iso3166.countries])
    default = models.BooleanField(default=False, verbose_name="Défaut")

    def __str__(self):
        return f"{self.user} - {self.name}"
