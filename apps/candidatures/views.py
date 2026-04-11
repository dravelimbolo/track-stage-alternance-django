from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView

from .forms import CandidatureForm
from .models import Candidature


class CandidatureMixin(LoginRequiredMixin):
    """Mixin commun : filtre automatiquement par utilisateur connecté."""

    def get_queryset(self):
        return Candidature.objects.filter(user=self.request.user)


class CandidatureListView(CandidatureMixin, ListView):
    model = Candidature
    template_name = "candidatures/list.html"
    context_object_name = "candidatures"
    paginate_by = 20

    def get_queryset(self):
        qs = super().get_queryset()
        statut = self.request.GET.get("statut")
        type_c = self.request.GET.get("type")
        q = self.request.GET.get("q")
        if statut:
            qs = qs.filter(statut=statut)
        if type_c:
            qs = qs.filter(type_contrat=type_c)
        if q:
            qs = qs.filter(entreprise__icontains=q) | qs.filter(poste__icontains=q)
        return qs

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["statuts"] = Candidature.Statut.choices
        ctx["types"] = Candidature.TypeContrat.choices
        ctx["current_statut"] = self.request.GET.get("statut", "")
        ctx["current_type"] = self.request.GET.get("type", "")
        ctx["q"] = self.request.GET.get("q", "")
        # Compteurs par statut
        base = Candidature.objects.filter(user=self.request.user)
        ctx["total"] = base.count()
        ctx["en_cours"] = base.filter(
            statut__in=["envoyee", "en_attente", "relancee", "entretien"]
        ).count()
        return ctx


class CandidatureDetailView(CandidatureMixin, DetailView):
    model = Candidature
    template_name = "candidatures/detail.html"
    context_object_name = "candidature"


class CandidatureCreateView(CandidatureMixin, CreateView):
    model = Candidature
    form_class = CandidatureForm
    template_name = "candidatures/form.html"
    success_url = reverse_lazy("candidatures:list")

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["title"] = "Nouvelle candidature"
        ctx["breadcrumb"] = [("Candidatures", "candidatures:list"), ("Nouvelle", None)]
        return ctx

    def form_valid(self, form):
        form.instance.user = self.request.user
        messages.success(self.request, "Candidature ajoutée avec succès !")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Erreur dans le formulaire. Vérifiez les champs obligatoires.")
        return super().form_invalid(form)


class CandidatureUpdateView(CandidatureMixin, UpdateView):
    model = Candidature
    form_class = CandidatureForm
    template_name = "candidatures/form.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["title"] = f"Modifier - {self.object}"
        ctx["breadcrumb"] = [
            ("Candidatures", "candidatures:list"),
            (str(self.object), "candidatures:detail"),
            ("Modifier", None),
        ]
        return ctx

    def form_valid(self, form):
        messages.success(self.request, "Candidature mise à jour.")
        return super().form_valid(form)


class CandidatureDeleteView(CandidatureMixin, DeleteView):
    model = Candidature
    template_name = "candidatures/confirm_delete.html"
    success_url = reverse_lazy("candidatures:list")
    context_object_name = "candidature"

    def form_valid(self, form):
        messages.success(self.request, "Candidature supprimée.")
        return super().form_valid(form)
