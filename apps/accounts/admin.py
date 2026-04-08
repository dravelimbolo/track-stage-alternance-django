from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ("email", "first_name", "last_name", "universite", "is_active", "date_joined")
    list_filter = ("is_active", "is_staff")
    search_fields = ("email", "first_name", "last_name")
    ordering = ("-date_joined",)
    fieldsets = BaseUserAdmin.fieldsets + (
        (
            "Profil TrackStage",
            {
                "fields": (
                    "avatar",
                    "bio",
                    "telephone",
                    "universite",
                    "formation",
                    "niveau",
                    "linkedin_url",
                    "github_url",
                    "notif_email_entretien",
                    "notif_email_relance",
                )
            },
        ),
    )
