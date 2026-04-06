from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    email = models.EmailField("adresse e-mail", unique=True)
    avatar = models.ImageField("avatar", upload_to="avatars/", blank=True, null=True)
    bio = models.TextField("biographie", blank=True)
    telephone = models.CharField("téléphone", max_length=20, blank=True)
    linkedin_url = models.URLField("profil LinkedIn", blank=True)
    github_url = models.URLField("profil GitHub", blank=True)
    universite = models.CharField("université / école", max_length=200, blank=True)
    formation = models.CharField("formation", max_length=200, blank=True)
    niveau = models.CharField("niveau d'études", max_length=50, blank=True)

    notif_email_entretien = models.BooleanField("notification e-mail entretien", default=True)
    notif_email_relance = models.BooleanField("notification e-mail relance", default=False)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    class Meta:
        verbose_name = "Utilisateur"
        verbose_name_plural = "Utilisateurs"

    def __str__(self):
        return self.get_full_name() or self.email

    @property
    def initiales(self):
        
        if self.first_name and self.last_name:
            return f"{self.first_name[0]}{self.last_name[0]}".upper()
        return self.email[:2].upper()

    @property
    def nom_affiche(self):
        return self.get_full_name() or self.email.split("@")[0]