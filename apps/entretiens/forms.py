from django import forms

from .models import Entretien

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


class EntretienForm(forms.ModelForm):
    class Meta:
        model = Entretien
        exclude = ["user", "created_at", "updated_at"]
        widgets = {
            "candidature": forms.Select(attrs={"class": SELECT}),
            "type_entretien": forms.Select(attrs={"class": SELECT}),
            "statut": forms.Select(attrs={"class": SELECT}),
            "date_heure": forms.DateTimeInput(
                attrs={"class": INPUT, "type": "datetime-local"},
                format="%Y-%m-%dT%H:%M",
            ),
            "duree_minutes": forms.NumberInput(
                attrs={"class": INPUT, "placeholder": "60", "min": 15, "step": 15}
            ),
            "lieu_ou_lien": forms.TextInput(
                attrs={"class": INPUT, "placeholder": "Adresse ou lien Meet/Zoom…"}
            ),
            "contact_nom": forms.TextInput(attrs={"class": INPUT, "placeholder": "Prénom Nom"}),
            "contact_poste": forms.TextInput(
                attrs={"class": INPUT, "placeholder": "ex : DRH, Lead Dev…"}
            ),
            "preparation": forms.Textarea(
                attrs={"class": TEXTAREA, "rows": 4, "placeholder": "Points à préparer…"}
            ),
            "retour": forms.Textarea(
                attrs={
                    "class": TEXTAREA,
                    "rows": 4,
                    "placeholder": "Ressenti, retour, points positifs/négatifs…",
                }
            ),
            "questions": forms.Textarea(
                attrs={
                    "class": TEXTAREA,
                    "rows": 4,
                    "placeholder": "Questions posées ou à préparer…",
                }
            ),
            "rappel_24h": forms.CheckboxInput(attrs={"class": "peer sr-only"}),
            "rappel_1h": forms.CheckboxInput(attrs={"class": "peer sr-only"}),
        }

    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        if user:
            # Ne montre que les candidatures de l'utilisateur connecté
            from apps.candidatures.models import Candidature

            self.fields["candidature"].queryset = Candidature.objects.filter(user=user)
        self.fields["date_heure"].input_formats = ["%Y-%m-%dT%H:%M"]
