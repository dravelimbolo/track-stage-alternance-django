import pytest
from django.test import Client
from django.urls import reverse

from apps.accounts.forms import RegisterForm
from apps.accounts.models import User


@pytest.fixture
def user(db):
    return User.objects.create_user(
        username="jean@example.com",
        email="jean@example.com",
        password="StrongPass123!",
        first_name="Jean",
        last_name="Dupont",
    )


class TestUserModel:
    def test_initiales_prenom_nom(self, user):
        assert user.initiales == "JD"

    def test_initiales_email_fallback(self, db):
        u = User.objects.create_user(
            username="ab@example.com",
            email="ab@example.com",
            password="pass",
        )
        assert u.initiales == "AB"

    def test_nom_affiche(self, user):
        assert user.nom_affiche == "Jean Dupont"

    def test_str(self, user):
        assert str(user) == "Jean Dupont"


class TestRegisterForm:
    def test_valid_form(self, db):
        data = {
            "first_name": "Alice",
            "last_name": "Martin",
            "email": "alice@example.com",
            "password1": "SecurePass42!",
            "password2": "SecurePass42!",
        }
        form = RegisterForm(data=data)
        assert form.is_valid()

    def test_passwords_mismatch(self, db):
        data = {
            "email": "test@ex.com",
            "password1": "pass1",
            "password2": "pass2",
        }
        form = RegisterForm(data=data)
        assert not form.is_valid()
        assert "password2" in form.errors

    def test_duplicate_email(self, user):
        data = {
            "email": "jean@example.com",
            "password1": "StrongPass123!",
            "password2": "StrongPass123!",
        }
        form = RegisterForm(data=data)
        assert not form.is_valid()
        assert "email" in form.errors


class TestAccountViews:
    def test_login_page_loads(self, db):
        c = Client()
        response = c.get(reverse("accounts:login"))
        assert response.status_code == 200

    def test_register_page_loads(self, db):
        c = Client()
        response = c.get(reverse("accounts:register"))
        assert response.status_code == 200

    def test_login_redirect_authenticated(self, user):
        c = Client()
        c.login(username="jean@example.com", password="StrongPass123!")
        response = c.get(reverse("accounts:login"))
        assert response.status_code == 302

    def test_profile_requires_login(self, db):
        c = Client()
        response = c.get(reverse("accounts:profile"))
        assert response.status_code == 302

    def test_profile_authenticated(self, user):
        c = Client()
        c.login(username="jean@example.com", password="StrongPass123!")
        response = c.get(reverse("accounts:profile"))
        assert response.status_code == 200

    def test_logout(self, user):
        c = Client()
        c.login(username="jean@example.com", password="StrongPass123!")
        response = c.post(reverse("accounts:logout"))
        assert response.status_code == 302
