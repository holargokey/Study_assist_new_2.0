from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse


User = get_user_model()


class AuthViewTests(TestCase):
    def test_register_creates_user_and_logs_them_in(self):
        response = self.client.post(
            reverse("register"),
            {
                "name": "Ada Lovelace",
                "email": "ada@example.com",
                "password": "AComplexPass123!",
                "next": reverse("home"),
            },
            follow=True,
        )

        self.assertEqual(response.status_code, 200)
        user = User.objects.get(email="ada@example.com")
        self.assertEqual(user.username, "ada@example.com")
        self.assertNotIn("_auth_user_id", self.client.session)
        self.assertContains(response, "Account created. Please sign in.")

    def test_register_success_message_is_not_rendered_in_page_flash_area(self):
        response = self.client.post(
            reverse("register"),
            {
                "name": "Katherine Johnson",
                "email": "katherine@example.com",
                "password": "AComplexPass123!",
                "next": reverse("home"),
            },
            follow=True,
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Account created. Please sign in.")
        self.assertContains(response, 'auth-signup-success')

    def test_login_uses_email_credentials(self):
        user = User.objects.create_user(
            username="grace@example.com",
            email="grace@example.com",
            password="AnotherPass123!",
        )

        response = self.client.post(
            reverse("login"),
            {
                "email": "grace@example.com",
                "password": "AnotherPass123!",
                "next": reverse("home"),
            },
        )

        self.assertRedirects(response, reverse("home"))
        self.assertEqual(int(self.client.session["_auth_user_id"]), user.pk)

    def test_register_validation_error_is_rendered_back_in_signup_modal(self):
        response = self.client.post(
            reverse("register"),
            {
                "name": "Ada Lovelace",
                "email": "ada@example.com",
                "password": "123",
                "next": reverse("home"),
            },
            follow=True,
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Password must be at least 8 characters.")
        self.assertContains(response, 'id="emailSignupModal"')

    def test_login_error_is_rendered_back_in_login_modal(self):
        response = self.client.post(
            reverse("login"),
            {
                "email": "missing@example.com",
                "password": "WrongPass123!",
                "next": reverse("home"),
            },
            follow=True,
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Invalid email or password.")
        self.assertContains(response, 'id="emailLoginModal"')

    def test_logout_clears_authenticated_session(self):
        user = User.objects.create_user(
            username="linus@example.com",
            email="linus@example.com",
            password="LogoutPass123!",
        )
        self.client.force_login(user)

        response = self.client.post(reverse("logout"), {"next": reverse("home")})

        self.assertRedirects(response, reverse("home"))
        self.assertNotIn("_auth_user_id", self.client.session)

    def test_logout_returns_sign_in_ui(self):
        user = User.objects.create_user(
            username="logout-ui@example.com",
            email="logout-ui@example.com",
            password="LogoutPass123!",
        )
        self.client.force_login(user)

        response = self.client.post(reverse("logout"), {"next": reverse("home")}, follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Sign in")
        self.assertNotContains(response, "Log out")


class AdminTests(TestCase):
    def test_admin_login_page_uses_custom_branding(self):
        response = self.client.get(reverse("admin:login"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "StudyAssists Admin")
