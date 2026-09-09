from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Q
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from cocktails.models import Cocktail, Equipment, Ingredient, Technique

from .models import LearningPath, Lesson, LessonProgress


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

    completed_lesson_ids: set[int] = set()

    if request.user.is_authenticated:
        completed_lesson_ids = set(
            LessonProgress.objects.filter(
                user=request.user,
                lesson__learning_path=learning_path,
                lesson__is_published=True,
            ).values_list(
                "lesson__pk",
                flat=True,
            )
        )
    total_lessons = len(lessons)
    completed_lessons = len(completed_lesson_ids)

    progress_percentage = round(completed_lessons / total_lessons * 100) if total_lessons else 0

    next_lesson = next(
        (lesson for lesson in lessons if lesson.pk not in completed_lesson_ids),
        None,
    )

    context = {
        "learning_path": learning_path,
        "lessons": lessons,
        "completed_lesson_ids": completed_lesson_ids,
        "completed_lessons": completed_lessons,
        "total_lessons": total_lessons,
        "progress_percentage": progress_percentage,
        "next_lesson": next_lesson,
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

    is_completed = False

    if request.user.is_authenticated:
        is_completed = LessonProgress.objects.filter(
            user=request.user,
            lesson=lesson,
        ).exists()

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
        "is_completed": is_completed,
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


@login_required
@require_POST
def toggle_lesson_completion(request, slug):
    lesson = get_object_or_404(
        Lesson,
        slug=slug,
        is_published=True,
        learning_path__is_published=True,
    )

    progress, created = LessonProgress.objects.get_or_create(
        user=request.user,
        lesson=lesson,
    )

    if created:
        messages.success(
            request,
            f'A aula "{lesson.title}" foi concluída.',
        )
    else:
        progress.delete()

        messages.success(
            request,
            f'A conclusão de "{lesson.title}" foi removida.',
        )

    return redirect(
        lesson.get_absolute_url(),
    )
