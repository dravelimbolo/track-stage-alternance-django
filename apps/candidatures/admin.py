from django.contrib import admin
from .models import Candidature


@admin.register(Candidature)
class CandidatureAdmin(admin.ModelAdmin):
    list_display = ("poste", "entreprise", "user", "statut", "type_contrat", "date_candidature", "created_at")
    list_filter = ("statut", "type_contrat", "secteur")
    search_fields = ("poste", "entreprise", "user__email")
    date_hierarchy = "created_at"
    readonly_fields = ("created_at", "updated_at")
    raw_id_fields = ("user",)
