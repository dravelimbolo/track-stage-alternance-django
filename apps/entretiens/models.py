from django.conf import settings
from django.db import models
from django.urls import reverse

from apps.candidatures.models import Candidature


class Entretien(models.Model):
    class Type(models.TextChoices):
        TELEPHONE = "telephone", "Téléphonique"
        VISIO = "visio", "Visioconférence"
        PRESENTIEL = "presentiel", "Présentiel"
        TECHNIQUE = "technique", "Technique"
        RH = "rh", "RH"
        FINAL = "final", "Final / Direction"

    class Statut(models.TextChoices):
        PLANIFIE = "planifie", "Planifié"
        PASSE = "passe", "Passé"
        ANNULE = "annule", "Annulé"
        REPORTE = "reporte", "Reporté"

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="entretiens",
    )
    candidature = models.ForeignKey(
        Candidature,
        on_delete=models.CASCADE,
        related_name="entretiens",
        null=True,
        blank=True,
    )

    type_entretien = models.CharField(
        "type", max_length=20, choices=Type.choices, default=Type.TELEPHONE
    )
    statut = models.CharField(
        "statut", max_length=20, choices=Statut.choices, default=Statut.PLANIFIE
    )

    date_heure = models.DateTimeField("date et heure")
    duree_minutes = models.PositiveIntegerField("durée (minutes)", default=60)

    lieu_ou_lien = models.CharField("lieu ou lien visio", max_length=500, blank=True)
    contact_nom = models.CharField("interlocuteur", max_length=200, blank=True)
    contact_poste = models.CharField("poste de l'interlocuteur", max_length=200, blank=True)

    preparation = models.TextField("notes de préparation", blank=True)
    retour = models.TextField("retour / ressenti post-entretien", blank=True)
    questions = models.TextField("questions posées / à préparer", blank=True)

    rappel_24h = models.BooleanField("rappel 24h avant", default=True)
    rappel_1h = models.BooleanField("rappel 1h avant", default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["date_heure"]
        verbose_name = "Entretien"
        verbose_name_plural = "Entretiens"

    def __str__(self):
        cand = str(self.candidature) if self.candidature else "sans candidature"
        return f"{self.get_type_entretien_display()} - {cand} ({self.date_heure:%d/%m/%Y %H:%M})"

    def get_absolute_url(self):
        return reverse("entretiens:detail", kwargs={"pk": self.pk})

    @property
    def entreprise(self):
        return self.candidature.entreprise if self.candidature else "-"

    @property
    def poste(self):
        return self.candidature.poste if self.candidature else "-"
