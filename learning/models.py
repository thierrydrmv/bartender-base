from django.db import models
from django.urls import reverse


class LearningPath(models.Model):
    title = models.CharField(max_length=120)
    slug = models.SlugField(max_length=140, unique=True)
    description = models.TextField()
    order = models.PositiveSmallIntegerField(default=0)
    is_published = models.BooleanField(default=False)

    class Meta:
        ordering = ["order", "title"]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse(
            "learning:path-detail",
            kwargs={"slug": self.slug},
        )


class Lesson(models.Model):
    class Difficulty(models.TextChoices):
        BEGINNER = "beginner", "Iniciante"
        INTERMEDIATE = "intermediate", "Intermediário"
        ADVANCED = "advanced", "Avançado"

    learning_path = models.ForeignKey(
        LearningPath,
        on_delete=models.CASCADE,
        related_name="lessons",
    )
    title = models.CharField(max_length=150)
    slug = models.SlugField(max_length=170, unique=True)
    summary = models.TextField()
    content = models.TextField()
    difficulty = models.CharField(
        max_length=20,
        choices=Difficulty.choices,
        default=Difficulty.BEGINNER,
    )
    reading_time = models.PositiveSmallIntegerField(default=5)
    order = models.PositiveSmallIntegerField(default=0)
    is_published = models.BooleanField(default=False)

    cocktails = models.ManyToManyField(
        "cocktails.Cocktail",
        related_name="lessons",
        blank=True,
    )
    ingredients = models.ManyToManyField(
        "cocktails.Ingredient",
        related_name="lessons",
        blank=True,
    )
    techniques = models.ManyToManyField(
        "cocktails.Technique",
        related_name="lessons",
        blank=True,
    )
    equipment = models.ManyToManyField(
        "cocktails.Equipment",
        related_name="lessons",
        blank=True,
    )

    class Meta:
        ordering = ["order", "title"]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse(
            "learning:lesson-detail",
            kwargs={"slug": self.slug},
        )
