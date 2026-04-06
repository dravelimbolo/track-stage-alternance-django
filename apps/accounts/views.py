from django.contrib.auth import login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.shortcuts import redirect
from django.views import View
from django.views.generic import FormView, UpdateView, TemplateView
from django.urls import reverse_lazy

from .forms import LoginEmailForm, RegisterForm, ProfileForm, NotificationsForm
from .models import User


class LoginView(FormView):
    template_name = "accounts/login.html"
    form_class = LoginEmailForm
    success_url = reverse_lazy("dashboard:index")

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect("dashboard:index")
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        user = form.user
        remember = form.cleaned_data.get("remember_me")
        if not remember:
            self.request.session.set_expiry(0)
        login(self.request, user, backend="django.contrib.auth.backends.ModelBackend")
        messages.success(self.request, f"Bienvenue, {user.nom_affiche} !")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Identifiants incorrects, veuillez réessayer.")
        return super().form_invalid(form)
  
    
class RegisterView(FormView):
    template_name = "accounts/register.html"
    form_class = RegisterForm
    success_url = reverse_lazy("dashboard:index")

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect("dashboard:index")
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        user = form.save()
        login(self.request, user, backend="django.contrib.auth.backends.ModelBackend")
        messages.success(self.request, "Compte créé avec succès. Bienvenue sur TrackStage !")
        return super().form_valid(form)


class LogoutView(View):
    def post(self, request):
        logout(request)
        messages.info(request, "Vous avez été déconnecté.")
        return redirect("accounts:login")


class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = "accounts/profile.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["profile_form"] = ProfileForm(instance=self.request.user)
        ctx["notif_form"] = NotificationsForm(instance=self.request.user)
        ctx["active_tab"] = self.request.GET.get("tab", "profil")
        return ctx

    def post(self, request, *args, **kwargs):
        tab = request.POST.get("tab", "profil")
        if tab == "profil":
            form = ProfileForm(request.POST, request.FILES, instance=request.user)
        else:
            form = NotificationsForm(request.POST, instance=request.user)

        if form.is_valid():
            form.save()
            messages.success(request, "Modifications enregistrées.")
        else:
            messages.error(request, "Erreur lors de la sauvegarde. Vérifiez les champs.")
        return redirect(f"{request.path}?tab={tab}")
