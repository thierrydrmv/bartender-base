from django.contrib.auth.models import User
from django.core import mail
from django.test import TestCase, override_settings
from django.urls import reverse


class AccountManagementTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(
            username="thierry",
            email="thierry@example.com",
            password="old-password-123",
        )

        cls.other_user = User.objects.create_user(
            username="other",
            email="other@example.com",
            password="other-password-123",
        )

    def test_update_profile_requires_authentication(self):
        response = self.client.get(
            reverse("accounts:update-profile"),
        )

        self.assertEqual(response.status_code, 302)

    def test_user_can_update_username_and_email(self):
        self.client.force_login(self.user)

        response = self.client.post(
            reverse("accounts:update-profile"),
            {
                "username": "thierry-updated",
                "email": "UPDATED@example.com",
            },
        )

        self.assertRedirects(
            response,
            reverse("accounts:profile"),
        )

        self.user.refresh_from_db()

        self.assertEqual(
            self.user.username,
            "thierry-updated",
        )
        self.assertEqual(
            self.user.email,
            "updated@example.com",
        )

    def test_duplicate_email_is_rejected(self):
        self.client.force_login(self.user)

        response = self.client.post(
            reverse("accounts:update-profile"),
            {
                "username": self.user.username,
                "email": self.other_user.email,
            },
        )

        self.assertEqual(response.status_code, 200)

        form = response.context["form"]

        self.assertIn("email", form.errors)
        self.assertEqual(
            form.errors["email"],
            ["Já existe uma conta com este e-mail."],
        )

    def test_user_can_change_password(self):
        self.client.force_login(self.user)

        response = self.client.post(
            reverse("accounts:password-change"),
            {
                "old_password": "old-password-123",
                "new_password1": "new-strong-password-456",
                "new_password2": "new-strong-password-456",
            },
        )

        self.assertRedirects(
            response,
            reverse("accounts:profile"),
        )

        self.user.refresh_from_db()

        self.assertTrue(self.user.check_password("new-strong-password-456"))

    @override_settings(EMAIL_BACKEND=("django.core.mail.backends.locmem.EmailBackend"))
    def test_password_reset_sends_email(self):
        response = self.client.post(
            reverse("accounts:password-reset"),
            {
                "email": self.user.email,
            },
        )

        self.assertRedirects(
            response,
            reverse("accounts:password-reset-done"),
        )
        self.assertEqual(len(mail.outbox), 1)
        self.assertIn(
            "Redefinição de senha",
            mail.outbox[0].subject,
        )
