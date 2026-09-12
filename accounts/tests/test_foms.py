from django.contrib.auth.models import User
from django.test import TestCase

from accounts.forms import RegisterForm, UserUpdateForm


class RegisterFormTests(TestCase):
    def test_form_is_valid_with_correct_data(self):
        form = RegisterForm(
            data={
                "username": "new-user",
                "email": "new-user@example.com",
                "password1": "Strong-password-123",
                "password2": "Strong-password-123",
            }
        )

        self.assertTrue(form.is_valid())

    def test_form_converts_email_to_lowercase(self):
        form = RegisterForm(
            data={
                "username": "new-user",
                "email": "NEW-USER@EXAMPLE.COM",
                "password1": "Strong-password-123",
                "password2": "Strong-password-123",
            }
        )

        self.assertTrue(form.is_valid())
        self.assertEqual(
            form.cleaned_data["email"],
            "new-user@example.com",
        )

    def test_form_rejects_duplicate_email_case_insensitively(self):
        User.objects.create_user(
            username="existing-user",
            email="existing@example.com",
            password="Strong-password-123",
        )

        form = RegisterForm(
            data={
                "username": "new-user",
                "email": "EXISTING@example.com",
                "password1": "Strong-password-456",
                "password2": "Strong-password-456",
            }
        )

        self.assertFalse(form.is_valid())
        self.assertEqual(
            form.errors["email"],
            ["Já existe uma conta com este e-mail."],
        )

    def test_form_rejects_different_passwords(self):
        form = RegisterForm(
            data={
                "username": "new-user",
                "email": "new-user@example.com",
                "password1": "Strong-password-123",
                "password2": "Different-password-456",
            }
        )

        self.assertFalse(form.is_valid())
        self.assertIn("password2", form.errors)

    def test_save_creates_user_with_email(self):
        form = RegisterForm(
            data={
                "username": "new-user",
                "email": "NEW-USER@EXAMPLE.COM",
                "password1": "Strong-password-123",
                "password2": "Strong-password-123",
            }
        )

        self.assertTrue(form.is_valid())

        user = form.save()

        self.assertTrue(User.objects.filter(pk=user.pk).exists())
        self.assertEqual(user.email, "new-user@example.com")
        self.assertTrue(user.check_password("Strong-password-123"))

    def test_save_with_commit_false_does_not_create_user(self):
        form = RegisterForm(
            data={
                "username": "new-user",
                "email": "new-user@example.com",
                "password1": "Strong-password-123",
                "password2": "Strong-password-123",
            }
        )

        self.assertTrue(form.is_valid())

        user = form.save(commit=False)

        self.assertIsNone(user.pk)
        self.assertEqual(user.email, "new-user@example.com")
        self.assertFalse(User.objects.filter(username="new-user").exists())


class UserUpdateFormTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(
            username="thierry",
            email="thierry@example.com",
            password="Strong-password-123",
        )
        cls.other_user = User.objects.create_user(
            username="other-user",
            email="other@example.com",
            password="Strong-password-456",
        )

    def test_form_updates_username_and_email(self):
        form = UserUpdateForm(
            data={
                "username": "thierry-updated",
                "email": "UPDATED@EXAMPLE.COM",
            },
            instance=self.user,
        )

        self.assertTrue(form.is_valid())

        user = form.save()

        self.assertEqual(user.username, "thierry-updated")
        self.assertEqual(user.email, "updated@example.com")

    def test_form_allows_user_to_keep_current_email(self):
        form = UserUpdateForm(
            data={
                "username": self.user.username,
                "email": "THIERRY@EXAMPLE.COM",
            },
            instance=self.user,
        )

        self.assertTrue(form.is_valid())
        self.assertEqual(
            form.cleaned_data["email"],
            "thierry@example.com",
        )

    def test_form_rejects_another_users_email(self):
        form = UserUpdateForm(
            data={
                "username": self.user.username,
                "email": "OTHER@EXAMPLE.COM",
            },
            instance=self.user,
        )

        self.assertFalse(form.is_valid())
        self.assertEqual(
            form.errors["email"],
            ["Já existe uma conta com este e-mail."],
        )
