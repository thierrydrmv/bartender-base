from django.test import TestCase
from django.urls import reverse

from learning.models import LearningPath, Lesson


class LearningViewTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.published_path = LearningPath.objects.create(
            title="Fundamentos",
            slug="fundamentos",
            description="Conhecimentos fundamentais.",
            order=1,
            is_published=True,
        )

        cls.unpublished_path = LearningPath.objects.create(
            title="Trilha secreta",
            slug="trilha-secreta",
            description="Conteúdo não publicado.",
            order=2,
            is_published=False,
        )

        cls.first_lesson = Lesson.objects.create(
            learning_path=cls.published_path,
            title="Organização do bar",
            slug="organizacao-do-bar",
            summary="Organize sua estação.",
            content="Conteúdo da primeira aula.",
            difficulty=Lesson.Difficulty.BEGINNER,
            reading_time=5,
            order=1,
            is_published=True,
        )

        cls.second_lesson = Lesson.objects.create(
            learning_path=cls.published_path,
            title="Mise en place",
            slug="mise-en-place",
            summary="Prepare tudo antes do serviço.",
            content="Conteúdo da segunda aula.",
            difficulty=Lesson.Difficulty.BEGINNER,
            reading_time=6,
            order=2,
            is_published=True,
        )

        cls.unpublished_lesson = Lesson.objects.create(
            learning_path=cls.published_path,
            title="Aula secreta",
            slug="aula-secreta",
            summary="Ainda não disponível.",
            content="Rascunho.",
            difficulty=Lesson.Difficulty.ADVANCED,
            reading_time=5,
            order=3,
            is_published=False,
        )

    def test_learning_path_list_returns_success(self):
        response = self.client.get(
            reverse("learning:path-list"),
        )

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response,
            "learning/learning_path_list.html",
        )

    def test_list_displays_only_published_paths(self):
        response = self.client.get(
            reverse("learning:path-list"),
        )

        self.assertContains(response, "Fundamentos")
        self.assertNotContains(response, "Trilha secreta")

    def test_learning_path_detail_displays_published_lessons(self):
        response = self.client.get(
            self.published_path.get_absolute_url(),
        )

        self.assertContains(response, "Organização do bar")
        self.assertContains(response, "Mise en place")
        self.assertNotContains(response, "Aula secreta")

    def test_unpublished_path_returns_404(self):
        response = self.client.get(
            self.unpublished_path.get_absolute_url(),
        )

        self.assertEqual(response.status_code, 404)

    def test_published_lesson_returns_success(self):
        response = self.client.get(
            self.first_lesson.get_absolute_url(),
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Conteúdo da primeira aula")

    def test_unpublished_lesson_returns_404(self):
        response = self.client.get(
            self.unpublished_lesson.get_absolute_url(),
        )

        self.assertEqual(response.status_code, 404)

    def test_first_lesson_has_next_lesson(self):
        response = self.client.get(
            self.first_lesson.get_absolute_url(),
        )

        self.assertEqual(
            response.context["next_lesson"],
            self.second_lesson,
        )
        self.assertIsNone(
            response.context["previous_lesson"],
        )

    def test_second_lesson_has_previous_lesson(self):
        response = self.client.get(
            self.second_lesson.get_absolute_url(),
        )

        self.assertEqual(
            response.context["previous_lesson"],
            self.first_lesson,
        )
        self.assertIsNone(
            response.context["next_lesson"],
        )
