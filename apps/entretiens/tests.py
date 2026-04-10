import pytest
from django.test import Client
from django.urls import reverse
from django.utils import timezone

from apps.accounts.models import User
from apps.candidatures.models import Candidature
from apps.entretiens.models import Entretien


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


@pytest.fixture
def entretien(user, candidature, db):
    return Entretien.objects.create(
        user=user,
        candidature=candidature,
        type_entretien=Entretien.Type.TELEPHONE,
        statut=Entretien.Statut.PLANIFIE,
        date_heure=timezone.now() + timezone.timedelta(days=3),
        duree_minutes=60,
    )


class TestEntretienModel:
    def test_str(self, entretien):
        result = str(entretien)
        assert "Téléphonique" in result
        assert "TechNova" in result

    def test_str_sans_candidature(self, user, db):
        e = Entretien.objects.create(
            user=user,
            candidature=None,
            type_entretien=Entretien.Type.RH,
            statut=Entretien.Statut.PLANIFIE,
            date_heure=timezone.now() + timezone.timedelta(days=1),
        )
        assert "sans candidature" in str(e)

    def test_get_absolute_url(self, entretien):
        url = entretien.get_absolute_url()
        assert str(entretien.pk) in url

    def test_entreprise_property(self, entretien):
        assert entretien.entreprise == "TechNova"

    def test_poste_property(self, entretien):
        assert entretien.poste == "Développeur Python"

    def test_entreprise_property_sans_candidature(self, user, db):
        e = Entretien.objects.create(
            user=user,
            candidature=None,
            type_entretien=Entretien.Type.RH,
            statut=Entretien.Statut.PLANIFIE,
            date_heure=timezone.now() + timezone.timedelta(days=1),
        )
        assert e.entreprise == "-"
        assert e.poste == "-"

    def test_ordering_par_date(self, user, candidature, db):
        Entretien.objects.create(
            user=user,
            candidature=candidature,
            type_entretien=Entretien.Type.RH,
            statut=Entretien.Statut.PLANIFIE,
            date_heure=timezone.now() + timezone.timedelta(days=5),
        )
        e2 = Entretien.objects.create(
            user=user,
            candidature=candidature,
            type_entretien=Entretien.Type.TECHNIQUE,
            statut=Entretien.Statut.PLANIFIE,
            date_heure=timezone.now() + timezone.timedelta(days=1),
        )
        entretiens = list(Entretien.objects.filter(user=user))
        assert entretiens[0].pk == e2.pk  # le plus proche en premier


class TestEntretienViews:
    def test_list_requires_login(self, db):
        c = Client()
        url = reverse("entretiens:list")
        response = c.get(url)
        assert response.status_code == 302
        assert "/auth/login" in response["Location"] or response["Location"].startswith("/")

    def test_list_authenticated(self, client_logged):
        url = reverse("entretiens:list")
        response = client_logged.get(url)
        assert response.status_code == 200

    def test_list_ne_montre_que_ses_entretiens(self, client_logged, entretien, db):
        other = User.objects.create_user(
            username="other@example.com",
            email="other@example.com",
            password="pass",
        )
        candidature_other = Candidature.objects.create(
            user=other,
            entreprise="AutreCorp",
            poste="Dev",
            type_contrat=Candidature.TypeContrat.CDI,
            statut=Candidature.Statut.ENVOYEE,
        )
        Entretien.objects.create(
            user=other,
            candidature=candidature_other,
            type_entretien=Entretien.Type.RH,
            statut=Entretien.Statut.PLANIFIE,
            date_heure=timezone.now() + timezone.timedelta(days=2),
        )
        url = reverse("entretiens:list")
        response = client_logged.get(url)
        assert response.status_code == 200
        for e in response.context["entretiens"]:
            assert e.user.username == "test@example.com"

    def test_create_get(self, client_logged):
        url = reverse("entretiens:create")
        response = client_logged.get(url)
        assert response.status_code == 200

    def test_create_form_filtre_candidatures_par_user(self, client_logged, candidature, db):
        other = User.objects.create_user(
            username="other@example.com",
            email="other@example.com",
            password="pass",
        )
        Candidature.objects.create(
            user=other,
            entreprise="AutreCorp",
            poste="Dev",
            type_contrat=Candidature.TypeContrat.CDI,
            statut=Candidature.Statut.ENVOYEE,
        )
        url = reverse("entretiens:create")
        response = client_logged.get(url)
        form = response.context["form"]
        qs = form.fields["candidature"].queryset
        assert candidature in qs
        assert all(c.user.username == "test@example.com" for c in qs)

    def test_create_post_valid(self, client_logged, user, candidature):
        url = reverse("entretiens:create")
        data = {
            "candidature": candidature.pk,
            "type_entretien": "telephone",
            "statut": "planifie",
            "date_heure": "2099-12-01T10:00",
            "duree_minutes": 45,
            "lieu_ou_lien": "",
            "contact_nom": "",
            "contact_poste": "",
            "preparation": "",
            "retour": "",
            "questions": "",
            "rappel_24h": True,
            "rappel_1h": False,
        }
        response = client_logged.post(url, data)
        assert response.status_code == 302
        assert Entretien.objects.filter(user=user, type_entretien="telephone").exists()

    def test_create_post_invalid(self, client_logged):
        url = reverse("entretiens:create")
        response = client_logged.post(url, {})
        assert response.status_code == 200  # re-render avec erreurs

    def test_detail_owner(self, client_logged, entretien):
        url = reverse("entretiens:detail", kwargs={"pk": entretien.pk})
        response = client_logged.get(url)
        assert response.status_code == 200

    def test_detail_other_user(self, entretien, db):
        User.objects.create_user(
            username="other@example.com",
            email="other@example.com",
            password="pass",
        )
        c = Client()
        c.login(username="other@example.com", password="pass")
        url = reverse("entretiens:detail", kwargs={"pk": entretien.pk})
        response = c.get(url)
        assert response.status_code == 404  # ownership enforced

    def test_update_get(self, client_logged, entretien):
        url = reverse("entretiens:update", kwargs={"pk": entretien.pk})
        response = client_logged.get(url)
        assert response.status_code == 200

    def test_update_post(self, client_logged, entretien, candidature):
        url = reverse("entretiens:update", kwargs={"pk": entretien.pk})
        data = {
            "candidature": candidature.pk,
            "type_entretien": "technique",
            "statut": "passe",
            "date_heure": "2099-12-01T14:00",
            "duree_minutes": 90,
            "lieu_ou_lien": "https://meet.google.com/xyz",
            "contact_nom": "",
            "contact_poste": "",
            "preparation": "",
            "retour": "Très bon échange",
            "questions": "",
            "rappel_24h": True,
            "rappel_1h": False,
        }
        response = client_logged.post(url, data)
        assert response.status_code == 302
        entretien.refresh_from_db()
        assert entretien.type_entretien == "technique"
        assert entretien.statut == "passe"
        assert entretien.duree_minutes == 90
        assert entretien.retour == "Très bon échange"

    def test_delete(self, client_logged, entretien):
        url = reverse("entretiens:delete", kwargs={"pk": entretien.pk})
        response = client_logged.post(url)
        assert response.status_code == 302
        assert not Entretien.objects.filter(pk=entretien.pk).exists()

    def test_delete_other_user(self, entretien, db):
        User.objects.create_user(
            username="other@example.com",
            email="other@example.com",
            password="pass",
        )
        c = Client()
        c.login(username="other@example.com", password="pass")
        url = reverse("entretiens:delete", kwargs={"pk": entretien.pk})
        response = c.post(url)
        assert response.status_code == 404
        assert Entretien.objects.filter(pk=entretien.pk).exists()
