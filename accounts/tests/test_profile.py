from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from cocktails.models import Cocktail, Favorite, Glassware
from learning.models import LearningPath, Lesson, LessonProgress


class ProfileDashboardTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(
            username="student",
            email="student@example.com",
            password="strong-password-123",
        )

        cls.other_user = User.objects.create_user(
            username="other",
            email="other@example.com",
            password="strong-password-123",
        )

        cls.glassware = Glassware.objects.create(
            name="Copo do painel",
            slug="copo-do-painel",
        )

        cls.cocktail = Cocktail.objects.create(
            name="Cocktail do painel",
            slug="cocktail-do-painel",
            description="Cocktail usado nos testes.",
            instructions="Misture.",
            difficulty=Cocktail.Difficulty.EASY,
            glassware=cls.glassware,
            is_published=True,
        )

        cls.learning_path = LearningPath.objects.create(
            title="Trilha do painel",
            slug="trilha-do-painel",
            description="Trilha usada nos testes.",
            order=1,
            is_published=True,
        )

        cls.first_lesson = Lesson.objects.create(
            learning_path=cls.learning_path,
            title="Primeira aula do painel",
            slug="primeira-aula-do-painel",
            summary="Primeira aula.",
            content="Conteúdo.",
            difficulty=Lesson.Difficulty.BEGINNER,
            reading_time=5,
            order=1,
            is_published=True,
        )

        cls.second_lesson = Lesson.objects.create(
            learning_path=cls.learning_path,
            title="Segunda aula do painel",
            slug="segunda-aula-do-painel",
            summary="Segunda aula.",
            content="Conteúdo.",
            difficulty=Lesson.Difficulty.BEGINNER,
            reading_time=5,
            order=2,
            is_published=True,
        )

    def test_profile_requires_authentication(self):
        response = self.client.get(
            reverse("accounts:profile"),
        )

        expected_url = f"{reverse('accounts:login')}?next={reverse('accounts:profile')}"

        self.assertRedirects(response, expected_url)

    def test_profile_displays_favorite(self):
        Favorite.objects.create(
            user=self.user,
            cocktail=self.cocktail,
        )

        self.client.force_login(self.user)

        response = self.client.get(
            reverse("accounts:profile"),
        )

        self.assertContains(response, self.cocktail.name)

    def test_profile_calculates_path_progress(self):
        LessonProgress.objects.create(
            user=self.user,
            lesson=self.first_lesson,
        )

        self.client.force_login(self.user)

        response = self.client.get(
            reverse("accounts:profile"),
        )

        started_path = response.context["started_paths"][0]

        self.assertEqual(
            started_path["completed_count"],
            1,
        )
        self.assertEqual(
            started_path["total_count"],
            2,
        )
        self.assertEqual(
            started_path["progress_percentage"],
            50,
        )

    def test_profile_recommends_next_lesson(self):
        LessonProgress.objects.create(
            user=self.user,
            lesson=self.first_lesson,
        )

        self.client.force_login(self.user)

        response = self.client.get(
            reverse("accounts:profile"),
        )

        self.assertEqual(
            response.context["next_lesson"],
            self.second_lesson,
        )

    def test_profile_does_not_show_other_user_data(self):
        Favorite.objects.create(
            user=self.other_user,
            cocktail=self.cocktail,
        )
        LessonProgress.objects.create(
            user=self.other_user,
            lesson=self.first_lesson,
        )

        self.client.force_login(self.user)

        response = self.client.get(
            reverse("accounts:profile"),
        )

        self.assertNotContains(response, self.cocktail.name)
        self.assertEqual(
            response.context["completed_lesson_count"],
            0,
        )
