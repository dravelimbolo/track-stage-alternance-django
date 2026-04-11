"""
Tableau de bord — agrège les données de toutes les apps.
"""

from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count
from django.utils import timezone
from django.views.generic import TemplateView

from apps.candidatures.models import Candidature
from apps.entretiens.models import Entretien


class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = "dashboard/index.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        user = self.request.user
        now = timezone.now()

        candidatures = Candidature.objects.filter(user=user)
        entretiens = Entretien.objects.filter(user=user).select_related("candidature")

        # Statistiques globales
        ctx["total_candidatures"] = candidatures.count()
        ctx["en_cours"] = candidatures.filter(
            statut__in=["envoyee", "en_attente", "relancee", "entretien"]
        ).count()
        ctx["entretiens_planifies"] = entretiens.filter(
            date_heure__gte=now, statut="planifie"
        ).count()
        ctx["offres_recues"] = candidatures.filter(statut__in=["offre", "acceptee"]).count()

        # Dernières candidatures
        ctx["recent_candidatures"] = candidatures.select_related()[:8]

        # Prochains entretiens
        ctx["prochains_entretiens"] = entretiens.filter(
            date_heure__gte=now, statut="planifie"
        ).order_by("date_heure")[:5]

        # Répartition par statut
        ctx["repartition_statuts"] = (
            candidatures.values("statut").annotate(total=Count("id")).order_by("-total")
        )

        return ctx
