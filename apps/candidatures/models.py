from django.conf import settings
from django.db import models
from django.urls import reverse


class Candidature(models.Model):
    class Statut(models.TextChoices):
        BROUILLON = "brouillon", "Brouillon"
        ENVOYEE = "envoyee", "Envoyée"
        EN_ATTENTE = "en_attente", "En attente"
        RELANCEE = "relancee", "Relancée"
        ENTRETIEN = "entretien", "Entretien"
        OFFRE = "offre", "Offre reçue"
        ACCEPTEE = "acceptee", "Acceptée"
        REFUSEE = "refusee", "Refusée"

    class TypeContrat(models.TextChoices):
        STAGE = "stage", "Stage"
        ALTERNANCE = "alternance", "Alternance"
        CDI = "cdi", "CDI"
        CDD = "cdd", "CDD"

    class Teletravail(models.TextChoices):
        PRESENTIEL = "presentiel", "Présentiel"
        HYBRIDE = "hybride", "Hybride"
        FULL_REMOTE = "remote", "Full remote"

    class Secteur(models.TextChoices):
        TECH = "tech", "Informatique / Tech"
        FINANCE = "finance", "Finance / Banque"
        SANTE = "sante", "Santé / Pharma"
        INDUSTRIE = "industrie", "Industrie"
        MARKETING = "marketing", "Marketing / Communication"
        CONSEIL = "conseil", "Conseil"
        AUTRE = "autre", "Autre"

    # Relations
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="candidatures",
    )

    # Entreprise
    entreprise = models.CharField("entreprise", max_length=200)
    secteur = models.CharField("secteur", max_length=20, choices=Secteur.choices, blank=True)
    site_web = models.URLField("site web", blank=True)
    lieu = models.CharField("lieu / ville", max_length=200, blank=True)
    teletravail = models.CharField(
        "télétravail", max_length=20, choices=Teletravail.choices, blank=True
    )

    # Poste
    poste = models.CharField("intitulé du poste", max_length=200)
    type_contrat = models.CharField(
        "type de contrat", max_length=20, choices=TypeContrat.choices, default=TypeContrat.STAGE
    )
    duree_contrat = models.CharField("durée", max_length=100, blank=True)
    date_debut = models.DateField("date de début souhaitée", null=True, blank=True)
    remuneration = models.CharField("rémunération", max_length=100, blank=True)
    lien_offre = models.URLField("lien de l'offre", blank=True)

    # Suivi
    statut = models.CharField(
        "statut", max_length=20, choices=Statut.choices, default=Statut.BROUILLON
    )
    date_candidature = models.DateField("date de candidature", null=True, blank=True)
    date_relance = models.DateField("date de relance prévue", null=True, blank=True)

    # Contact recruteur
    contact_nom = models.CharField("nom du contact", max_length=200, blank=True)
    contact_email = models.EmailField("e-mail du contact", blank=True)
    contact_linkedin = models.URLField("LinkedIn du contact", blank=True)

    # Contenu
    notes = models.TextField("notes & remarques", blank=True)
    lettre_motivation = models.TextField("lettre de motivation", blank=True)

    # Métadonnées
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Candidature"
        verbose_name_plural = "Candidatures"

    def __str__(self):
        return f"{self.poste} @ {self.entreprise}"

    def get_absolute_url(self):
        return reverse("candidatures:detail", kwargs={"pk": self.pk})

    # Utilitaires de couleur pour les badges
    STATUT_COLORS = {
        "brouillon": ("bg-gray-100", "text-gray-700"),
        "envoyee": ("bg-blue-100", "text-blue-700"),
        "en_attente": ("bg-yellow-100", "text-yellow-800"),
        "relancee": ("bg-orange-100", "text-orange-700"),
        "entretien": ("bg-purple-100", "text-purple-700"),
        "offre": ("bg-green-100", "text-green-700"),
        "acceptee": ("bg-green-200", "text-green-800"),
        "refusee": ("bg-red-100", "text-red-700"),
    }

    @property
    def statut_bg(self):
        return self.STATUT_COLORS.get(self.statut, ("bg-gray-100", "text-gray-700"))[0]

    @property
    def statut_text(self):
        return self.STATUT_COLORS.get(self.statut, ("bg-gray-100", "text-gray-700"))[1]
