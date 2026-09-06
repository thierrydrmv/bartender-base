from django.test import TestCase
from django.urls import reverse

from learning.models import LearningPath, Lesson


class LearningModelTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.learning_path = LearningPath.objects.create(
            title="Fundamentos da profissão",
            slug="fundamentos",
            description="Conhecimentos iniciais para bartenders.",
            order=1,
            is_published=True,
        )

        cls.lesson = Lesson.objects.create(
            learning_path=cls.learning_path,
            title="Organização do bar",
            slug="organizacao-do-bar",
            summary="Aprenda a organizar sua estação.",
            content="Conteúdo completo da aula.",
            difficulty=Lesson.Difficulty.BEGINNER,
            reading_time=5,
            order=1,
            is_published=True,
        )

    def test_learning_path_string_representation(self):
        self.assertEqual(
            str(self.learning_path),
            "Fundamentos da profissão",
        )

    def test_lesson_string_representation(self):
        self.assertEqual(
            str(self.lesson),
            "Organização do bar",
        )

    def test_learning_path_absolute_url(self):
        expected_url = reverse(
            "learning:path-detail",
            kwargs={"slug": "fundamentos"},
        )

        self.assertEqual(
            self.learning_path.get_absolute_url(),
            expected_url,
        )

    def test_lesson_absolute_url(self):
        expected_url = reverse(
            "learning:lesson-detail",
            kwargs={"slug": "organizacao-do-bar"},
        )

        self.assertEqual(
            self.lesson.get_absolute_url(),
            expected_url,
        )
