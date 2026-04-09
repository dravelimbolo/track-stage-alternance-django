from django import forms

from .models import Candidature

INPUT = (
    "w-full h-11 px-4 rounded border-2 border-[#E0E0E0] bg-white text-sm "
    "font-medium text-[#1A1A1A] focus:outline-none focus:border-[#E8B800] "
    "placeholder-[#1A1A1A]/30 transition-colors"
)
SELECT = (
    "w-full h-11 px-4 rounded border-2 border-[#E0E0E0] bg-white text-sm "
    "font-medium text-[#1A1A1A] focus:outline-none focus:border-[#E8B800] "
    "transition-colors appearance-none"
)
TEXTAREA = (
    "w-full px-4 py-3 rounded border-2 border-[#E0E0E0] bg-white text-sm "
    "font-medium text-[#1A1A1A] focus:outline-none focus:border-[#E8B800] "
    "placeholder-[#1A1A1A]/30 transition-colors resize-none"
)


class CandidatureForm(forms.ModelForm):
    class Meta:
        model = Candidature
        exclude = ["user", "created_at", "updated_at"]
        widgets = {
            "entreprise": forms.TextInput(
                attrs={"class": INPUT, "placeholder": "ex : TechNova SAS"}
            ),
            "secteur": forms.Select(attrs={"class": SELECT}),
            "site_web": forms.URLInput(
                attrs={"class": INPUT, "placeholder": "https://entreprise.com"}
            ),
            "lieu": forms.TextInput(attrs={"class": INPUT, "placeholder": "ex : Paris, Lyon…"}),
            "teletravail": forms.Select(attrs={"class": SELECT}),
            "poste": forms.TextInput(
                attrs={"class": INPUT, "placeholder": "ex : Développeur Fullstack"}
            ),
            "type_contrat": forms.Select(attrs={"class": SELECT}),
            "duree_contrat": forms.TextInput(attrs={"class": INPUT, "placeholder": "ex : 6 mois"}),
            "date_debut": forms.DateInput(attrs={"class": INPUT, "type": "date"}),
            "remuneration": forms.TextInput(
                attrs={"class": INPUT, "placeholder": "ex : 800 €/mois"}
            ),
            "lien_offre": forms.URLInput(attrs={"class": INPUT, "placeholder": "https://…"}),
            "statut": forms.Select(attrs={"class": SELECT}),
            "date_candidature": forms.DateInput(attrs={"class": INPUT, "type": "date"}),
            "date_relance": forms.DateInput(attrs={"class": INPUT, "type": "date"}),
            "contact_nom": forms.TextInput(attrs={"class": INPUT, "placeholder": "Prénom Nom"}),
            "contact_email": forms.EmailInput(
                attrs={"class": INPUT, "placeholder": "recruteur@entreprise.com"}
            ),
            "contact_linkedin": forms.URLInput(
                attrs={"class": INPUT, "placeholder": "https://linkedin.com/in/…"}
            ),
            "notes": forms.Textarea(
                attrs={"class": TEXTAREA, "rows": 4, "placeholder": "Notes libres…"}
            ),
            "lettre_motivation": forms.Textarea(
                attrs={"class": TEXTAREA, "rows": 8, "placeholder": "Votre lettre de motivation…"}
            ),
        }
