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
