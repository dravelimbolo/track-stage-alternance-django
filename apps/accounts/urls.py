from django.urls import path

from . import views

app_name = "accounts"

urlpatterns = [
    path("", views.LoginView.as_view(), name="login"),
    path("inscription/", views.RegisterView.as_view(), name="register"),
    path("deconnexion/", views.LogoutView.as_view(), name="logout"),
    path("profil/", views.ProfileView.as_view(), name="profile"),
]
