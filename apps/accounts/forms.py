from django import forms
from django.contrib.auth import authenticate

from .models import User


class LoginEmailForm(forms.Form):
    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={
                "placeholder": "Adresse e-mail",
                "class": "w-full h-12 px-4 rounded-lg border-2 border-[#E0E0E0] bg-white text-sm font-medium text-[#1A1A1A] focus:outline-none focus:border-[#E8B800] placeholder-gray-400 transition-colors",
                "autocomplete": "email",
            }
        )
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "Mot de passe",
                "class": "w-full h-12 px-4 rounded-lg border-2 border-[#E0E0E0] bg-white text-sm font-medium text-[#1A1A1A] focus:outline-none focus:border-[#E8B800] placeholder-gray-400 transition-colors",
                "autocomplete": "current-password",
            }
        )
    )
    remember_me = forms.BooleanField(required=False)

    def clean(self):
        cleaned = super().clean()
        email = cleaned.get("email")
        password = cleaned.get("password")
        if email and password:
            self.user = authenticate(username=email, password=password)
            if self.user is None:
                raise forms.ValidationError("Email ou mot de passe incorrect.")
            if not self.user.is_active:
                raise forms.ValidationError("Ce compte est désactivé.")
        return cleaned


INPUT_CLASS = (
    "w-full px-4 py-3 rounded-lg border-2 border-[#E0E0E0] bg-white text-sm "
    "font-medium text-[#1A1A1A] focus:outline-none focus:border-[#E8B800] "
    "placeholder-gray-400 transition-colors"
)


class RegisterForm(forms.ModelForm):
    password1 = forms.CharField(
        label="Mot de passe",
        widget=forms.PasswordInput(attrs={"placeholder": "Mot de passe", "class": INPUT_CLASS}),
    )
    password2 = forms.CharField(
        label="Confirmer le mot de passe",
        widget=forms.PasswordInput(
            attrs={"placeholder": "Confirmer le mot de passe", "class": INPUT_CLASS}
        ),
    )

    class Meta:
        model = User
        fields = ["first_name", "last_name", "email"]
        widgets = {
            "first_name": forms.TextInput(attrs={"placeholder": "Prénom", "class": INPUT_CLASS}),
            "last_name": forms.TextInput(attrs={"placeholder": "Nom", "class": INPUT_CLASS}),
            "email": forms.EmailInput(
                attrs={"placeholder": "Adresse e-mail", "class": INPUT_CLASS}
            ),
        }

    def clean_email(self):
        email = self.cleaned_data["email"]
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Un compte existe déjà avec cet e-mail.")
        return email

    def clean(self):
        cleaned = super().clean()
        p1 = cleaned.get("password1")
        p2 = cleaned.get("password2")
        if p1 and p2 and p1 != p2:
            self.add_error("password2", "Les mots de passe ne correspondent pas.")
        return cleaned

    def save(self, commit=True):
        user = super().save(commit=False)
        user.username = self.cleaned_data["email"]
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


FIELD_CLASS = (
    "w-full h-11 px-4 rounded border-2 border-[#E0E0E0] bg-white text-sm "
    "font-medium text-[#1A1A1A] focus:outline-none focus:border-[#E8B800] "
    "placeholder-[#1A1A1A]/30 transition-colors"
)


class ProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = [
            "first_name",
            "last_name",
            "email",
            "telephone",
            "bio",
            "universite",
            "formation",
            "niveau",
            "linkedin_url",
            "github_url",
            "avatar",
        ]
        widgets = {
            "first_name": forms.TextInput(attrs={"class": FIELD_CLASS, "placeholder": "Prénom"}),
            "last_name": forms.TextInput(attrs={"class": FIELD_CLASS, "placeholder": "Nom"}),
            "email": forms.EmailInput(attrs={"class": FIELD_CLASS}),
            "telephone": forms.TextInput(
                attrs={"class": FIELD_CLASS, "placeholder": "ex : +33 6 12 34 56 78"}
            ),
            "bio": forms.Textarea(
                attrs={
                    "class": FIELD_CLASS + " h-24 resize-none py-3",
                    "placeholder": "Quelques mots sur vous…",
                    "rows": 3,
                }
            ),
            "universite": forms.TextInput(
                attrs={"class": FIELD_CLASS, "placeholder": "ex : Université Paris-Saclay"}
            ),
            "formation": forms.TextInput(
                attrs={"class": FIELD_CLASS, "placeholder": "ex : Master Informatique"}
            ),
            "niveau": forms.TextInput(attrs={"class": FIELD_CLASS, "placeholder": "ex : M2, L3…"}),
            "linkedin_url": forms.URLInput(
                attrs={"class": FIELD_CLASS, "placeholder": "https://linkedin.com/in/…"}
            ),
            "github_url": forms.URLInput(
                attrs={"class": FIELD_CLASS, "placeholder": "https://github.com/…"}
            ),
        }


class NotificationsForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["notif_email_entretien", "notif_email_relance"]
