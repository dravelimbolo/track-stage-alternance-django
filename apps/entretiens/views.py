from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView

from .forms import EntretienForm
from .models import Entretien


class EntretienMixin(LoginRequiredMixin):
    def get_queryset(self):
        return Entretien.objects.filter(user=self.request.user).select_related("candidature")


class EntretienListView(EntretienMixin, ListView):
    model = Entretien
    template_name = "entretiens/list.html"
    context_object_name = "entretiens"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        now = timezone.now()
        qs = self.get_queryset()
        ctx["a_venir"] = qs.filter(date_heure__gte=now, statut="planifie")
        ctx["passes"] = qs.filter(date_heure__lt=now).order_by("-date_heure")[:5]
        ctx["total"] = qs.count()
        return ctx


class EntretienDetailView(EntretienMixin, DetailView):
    model = Entretien
    template_name = "entretiens/detail.html"
    context_object_name = "entretien"


class EntretienCreateView(EntretienMixin, CreateView):
    model = Entretien
    form_class = EntretienForm
    template_name = "entretiens/form.html"
    success_url = reverse_lazy("entretiens:list")

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["title"] = "Planifier un entretien"
        return ctx

    def form_valid(self, form):
        form.instance.user = self.request.user
        messages.success(self.request, "Entretien planifié avec succès !")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Erreur dans le formulaire.")
        return super().form_invalid(form)


class EntretienUpdateView(EntretienMixin, UpdateView):
    model = Entretien
    form_class = EntretienForm
    template_name = "entretiens/form.html"

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["title"] = "Modifier l'entretien"
        return ctx

    def form_valid(self, form):
        messages.success(self.request, "Entretien mis à jour.")
        return super().form_valid(form)


class EntretienDeleteView(EntretienMixin, DeleteView):
    model = Entretien
    template_name = "entretiens/confirm_delete.html"
    success_url = reverse_lazy("entretiens:list")
    context_object_name = "entretien"

    def form_valid(self, form):
        messages.success(self.request, "Entretien supprimé.")
        return super().form_valid(form)
