import pytest
from django.test import Client
from django.urls import reverse

from apps.accounts.models import User
from apps.candidatures.models import Candidature


@pytest.fixture
def user(db):
    return User.objects.create_user(
        username="test@example.com",
        email="test@example.com",
        password="testpass123",
    )


@pytest.fixture
def client_logged(user):
    c = Client()
    c.login(username="test@example.com", password="testpass123")
    return c


@pytest.fixture
def candidature(user, db):
    return Candidature.objects.create(
        user=user,
        entreprise="TechNova",
        poste="Développeur Python",
        type_contrat=Candidature.TypeContrat.STAGE,
        statut=Candidature.Statut.ENVOYEE,
    )


class TestCandidatureModel:
    def test_str(self, candidature):
        assert "TechNova" in str(candidature)
        assert "Développeur Python" in str(candidature)

    def test_statut_colors_defined(self, candidature):
        assert candidature.statut_bg
        assert candidature.statut_text

    def test_get_absolute_url(self, candidature):
        url = candidature.get_absolute_url()
        assert str(candidature.pk) in url


class TestCandidatureViews:
    def test_list_requires_login(self, db):
        c = Client()
        url = reverse("candidatures:list")
        response = c.get(url)
        assert response.status_code == 302
        assert "/auth/login" in response["Location"] or response["Location"].startswith("/")

    def test_list_authenticated(self, client_logged):
        url = reverse("candidatures:list")
        response = client_logged.get(url)
        assert response.status_code == 200

    def test_create_get(self, client_logged):
        url = reverse("candidatures:create")
        response = client_logged.get(url)
        assert response.status_code == 200

    def test_create_post_valid(self, client_logged, user):
        url = reverse("candidatures:create")
        data = {
            "entreprise": "NewCorp",
            "poste": "Dev Junior",
            "type_contrat": "stage",
            "statut": "brouillon",
        }
        response = client_logged.post(url, data)
        assert response.status_code == 302
        assert Candidature.objects.filter(user=user, entreprise="NewCorp").exists()

    def test_create_post_invalid(self, client_logged):
        url = reverse("candidatures:create")
        response = client_logged.post(url, {})
        assert response.status_code == 200  # re-render with errors

    def test_detail_owner(self, client_logged, candidature):
        url = reverse("candidatures:detail", kwargs={"pk": candidature.pk})
        response = client_logged.get(url)
        assert response.status_code == 200

    def test_detail_other_user(self, candidature, db):
        User.objects.create_user(
            username="other@example.com",
            email="other@example.com",
            password="pass",
        )
        c = Client()
        c.login(username="other@example.com", password="pass")
        url = reverse("candidatures:detail", kwargs={"pk": candidature.pk})
        response = c.get(url)
        assert response.status_code == 404  # ownership enforced

    def test_update_post(self, client_logged, candidature):
        url = reverse("candidatures:update", kwargs={"pk": candidature.pk})
        data = {
            "entreprise": "TechNova Updated",
            "poste": "Développeur Python",
            "type_contrat": "stage",
            "statut": "en_attente",
        }
        response = client_logged.post(url, data)
        assert response.status_code == 302
        candidature.refresh_from_db()
        assert candidature.entreprise == "TechNova Updated"
        assert candidature.statut == "en_attente"

    def test_delete(self, client_logged, candidature, user):
        url = reverse("candidatures:delete", kwargs={"pk": candidature.pk})
        response = client_logged.post(url)
        assert response.status_code == 302
        assert not Candidature.objects.filter(pk=candidature.pk).exists()
