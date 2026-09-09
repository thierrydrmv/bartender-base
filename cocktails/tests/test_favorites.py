from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from cocktails.models import Cocktail, Favorite, Glassware


class FavoriteTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(
            username="thierry",
            email="thierry@example.com",
            password="strong-password-123",
        )

        cls.other_user = User.objects.create_user(
            username="other",
            email="other@example.com",
            password="strong-password-123",
        )

        cls.glassware = Glassware.objects.create(
            name="Copo favorito",
            slug="copo-favorito",
        )

        cls.cocktail = Cocktail.objects.create(
            name="Cocktail favorito",
            slug="cocktail-favorito",
            description="Cocktail utilizado nos testes.",
            instructions="Misture os ingredientes.",
            difficulty=Cocktail.Difficulty.EASY,
            preparation_time=5,
            glassware=cls.glassware,
            is_published=True,
        )

    def get_toggle_url(self):
        return reverse(
            "cocktails:toggle-favorite",
            kwargs={"slug": self.cocktail.slug},
        )

    def test_authenticated_user_can_add_favorite(self):
        self.client.force_login(self.user)

        response = self.client.post(
            self.get_toggle_url(),
        )

        self.assertRedirects(
            response,
            self.cocktail.get_absolute_url(),
        )
        self.assertTrue(
            Favorite.objects.filter(
                user=self.user,
                cocktail=self.cocktail,
            ).exists()
        )

    def test_user_can_remove_favorite(self):
        Favorite.objects.create(
            user=self.user,
            cocktail=self.cocktail,
        )

        self.client.force_login(self.user)

        response = self.client.post(
            self.get_toggle_url(),
        )

        self.assertRedirects(
            response,
            self.cocktail.get_absolute_url(),
        )
        self.assertFalse(
            Favorite.objects.filter(
                user=self.user,
                cocktail=self.cocktail,
            ).exists()
        )

    def test_guest_is_redirected_to_login(self):
        response = self.client.post(
            self.get_toggle_url(),
        )

        expected_url = f"{reverse('accounts:login')}?next={self.get_toggle_url()}"

        self.assertRedirects(
            response,
            expected_url,
        )

    def test_favorite_action_only_accepts_post(self):
        self.client.force_login(self.user)

        response = self.client.get(
            self.get_toggle_url(),
        )

        self.assertEqual(response.status_code, 405)

    def test_favorites_are_isolated_by_user(self):
        Favorite.objects.create(
            user=self.other_user,
            cocktail=self.cocktail,
        )

        self.client.force_login(self.user)

        response = self.client.get(
            reverse("accounts:profile"),
        )

        self.assertNotContains(
            response,
            self.cocktail.name,
        )

    def test_profile_displays_user_favorite(self):
        Favorite.objects.create(
            user=self.user,
            cocktail=self.cocktail,
        )

        self.client.force_login(self.user)

        response = self.client.get(
            reverse("accounts:profile"),
        )

        self.assertContains(
            response,
            self.cocktail.name,
        )
        self.assertContains(
            response,
            self.cocktail.get_absolute_url(),
        )
