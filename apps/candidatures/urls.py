from django.urls import path

from . import views

app_name = "candidatures"

urlpatterns = [
    path("", views.CandidatureListView.as_view(), name="list"),
    path("nouvelle/", views.CandidatureCreateView.as_view(), name="create"),
    path("<int:pk>/", views.CandidatureDetailView.as_view(), name="detail"),
    path("<int:pk>/modifier/", views.CandidatureUpdateView.as_view(), name="update"),
    path("<int:pk>/supprimer/", views.CandidatureDeleteView.as_view(), name="delete"),
]
