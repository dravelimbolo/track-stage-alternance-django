from django.contrib import admin

from .models import Entretien


@admin.register(Entretien)
class EntretienAdmin(admin.ModelAdmin):
    list_display = ("__str__", "user", "type_entretien", "statut", "date_heure")
    list_filter = ("type_entretien", "statut")
    search_fields = ("candidature__entreprise", "candidature__poste", "user__email")
    date_hierarchy = "date_heure"
    raw_id_fields = ("user", "candidature")
