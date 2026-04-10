from django.urls import path

from . import views

app_name = "entretiens"

urlpatterns = [
    path("", views.EntretienListView.as_view(), name="list"),
    path("planifier/", views.EntretienCreateView.as_view(), name="create"),
    path("<int:pk>/", views.EntretienDetailView.as_view(), name="detail"),
    path("<int:pk>/modifier/", views.EntretienUpdateView.as_view(), name="update"),
    path("<int:pk>/supprimer/", views.EntretienDeleteView.as_view(), name="delete"),
]
