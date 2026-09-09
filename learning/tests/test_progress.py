from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from learning.models import LearningPath, Lesson, LessonProgress


class LessonProgressTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(
            username="student",
            email="student@example.com",
            password="strong-password-123",
        )

        cls.other_user = User.objects.create_user(
            username="other-student",
            email="other@example.com",
            password="strong-password-123",
        )

        cls.learning_path = LearningPath.objects.create(
            title="Trilha de teste",
            slug="trilha-de-teste",
            description="Trilha utilizada nos testes.",
            order=1,
            is_published=True,
        )

        cls.first_lesson = Lesson.objects.create(
            learning_path=cls.learning_path,
            title="Primeira aula",
            slug="primeira-aula-progress",
            summary="Resumo da primeira aula.",
            content="Conteúdo da primeira aula.",
            difficulty=Lesson.Difficulty.BEGINNER,
            reading_time=5,
            order=1,
            is_published=True,
        )

        cls.second_lesson = Lesson.objects.create(
            learning_path=cls.learning_path,
            title="Segunda aula",
            slug="segunda-aula-progress",
            summary="Resumo da segunda aula.",
            content="Conteúdo da segunda aula.",
            difficulty=Lesson.Difficulty.BEGINNER,
            reading_time=5,
            order=2,
            is_published=True,
        )

    def get_toggle_url(self, lesson):
        return reverse(
            "learning:toggle-completion",
            kwargs={"slug": lesson.slug},
        )

    def test_authenticated_user_can_complete_lesson(self):
        self.client.force_login(self.user)

        response = self.client.post(
            self.get_toggle_url(self.first_lesson),
        )

        self.assertRedirects(
            response,
            self.first_lesson.get_absolute_url(),
        )
        self.assertTrue(
            LessonProgress.objects.filter(
                user=self.user,
                lesson=self.first_lesson,
            ).exists()
        )

    def test_user_can_remove_completion(self):
        LessonProgress.objects.create(
            user=self.user,
            lesson=self.first_lesson,
        )

        self.client.force_login(self.user)

        self.client.post(
            self.get_toggle_url(self.first_lesson),
        )

        self.assertFalse(
            LessonProgress.objects.filter(
                user=self.user,
                lesson=self.first_lesson,
            ).exists()
        )

    def test_guest_is_redirected_to_login(self):
        toggle_url = self.get_toggle_url(self.first_lesson)

        response = self.client.post(toggle_url)

        expected_url = f"{reverse('accounts:login')}?next={toggle_url}"

        self.assertRedirects(
            response,
            expected_url,
        )

    def test_completion_only_accepts_post(self):
        self.client.force_login(self.user)

        response = self.client.get(
            self.get_toggle_url(self.first_lesson),
        )

        self.assertEqual(response.status_code, 405)

    def test_lesson_detail_reports_completion(self):
        LessonProgress.objects.create(
            user=self.user,
            lesson=self.first_lesson,
        )

        self.client.force_login(self.user)

        response = self.client.get(
            self.first_lesson.get_absolute_url(),
        )

        self.assertTrue(
            response.context["is_completed"],
        )

    def test_learning_path_calculates_progress(self):
        LessonProgress.objects.create(
            user=self.user,
            lesson=self.first_lesson,
        )

        self.client.force_login(self.user)

        response = self.client.get(
            self.learning_path.get_absolute_url(),
        )

        self.assertEqual(
            response.context["completed_lessons"],
            1,
        )
        self.assertEqual(
            response.context["total_lessons"],
            2,
        )
        self.assertEqual(
            response.context["progress_percentage"],
            50,
        )
        self.assertEqual(
            response.context["next_lesson"],
            self.second_lesson,
        )

    def test_progress_is_isolated_by_user(self):
        LessonProgress.objects.create(
            user=self.other_user,
            lesson=self.first_lesson,
        )

        self.client.force_login(self.user)

        response = self.client.get(
            self.learning_path.get_absolute_url(),
        )

        self.assertEqual(
            response.context["completed_lessons"],
            0,
        )
        self.assertEqual(
            response.context["progress_percentage"],
            0,
        )
