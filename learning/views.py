from django.db.models import Count, Q
from django.shortcuts import get_object_or_404, render

from cocktails.models import Cocktail, Equipment, Ingredient, Technique

from .models import LearningPath, Lesson


def learning_path_list(request):
    learning_paths = (
        LearningPath.objects.filter(is_published=True)
        .annotate(
            lesson_count=Count(
                "lessons",
                filter=Q(lessons__is_published=True),
            )
        )
        .order_by("order", "title")
    )

    context = {
        "learning_paths": learning_paths,
    }

    return render(
        request,
        "learning/learning_path_list.html",
        context,
    )


def learning_path_detail(request, slug):
    learning_path = get_object_or_404(
        LearningPath,
        slug=slug,
        is_published=True,
    )

    lessons = Lesson.objects.filter(
        learning_path=learning_path,
        is_published=True,
    ).order_by("order", "title")

    context = {
        "learning_path": learning_path,
        "lessons": lessons,
    }

    return render(
        request,
        "learning/learning_path_detail.html",
        context,
    )


def lesson_detail(request, slug):
    lesson = get_object_or_404(
        Lesson.objects.select_related("learning_path"),
        slug=slug,
        is_published=True,
        learning_path__is_published=True,
    )

    previous_lesson = (
        Lesson.objects.filter(
            learning_path=lesson.learning_path,
            is_published=True,
            order__lt=lesson.order,
        )
        .order_by("-order")
        .first()
    )

    next_lesson = (
        Lesson.objects.filter(
            learning_path=lesson.learning_path,
            is_published=True,
            order__gt=lesson.order,
        )
        .order_by("order")
        .first()
    )

    cocktails = Cocktail.objects.filter(
        lessons=lesson,
        is_published=True,
    ).distinct()

    techniques = Technique.objects.filter(
        lessons=lesson,
    ).distinct()

    equipments = Equipment.objects.filter(
        lessons=lesson,
    ).distinct()

    ingredients = Ingredient.objects.filter(
        lessons=lesson,
    ).distinct()

    context = {
        "lesson": lesson,
        "previous_lesson": previous_lesson,
        "next_lesson": next_lesson,
        "cocktails": cocktails,
        "techniques": techniques,
        "equipments": equipments,
        "ingredients": ingredients,
    }

    return render(
        request,
        "learning/lesson_detail.html",
        context,
    )
