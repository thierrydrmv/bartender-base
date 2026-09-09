# Create your views here.
from collections import defaultdict

from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from cocktails.models import Favorite
from learning.models import LearningPath, Lesson, LessonProgress

from .forms import RegisterForm


def register(request):
    if request.user.is_authenticated:
        return redirect("accounts:profile")

    form = RegisterForm(
        request.POST or None,
    )

    if request.method == "POST" and form.is_valid():
        user = form.save()
        login(request, user)

        return redirect("accounts:profile")

    return render(
        request,
        "accounts/register.html",
        {"form": form},
    )


@login_required
def profile(request):
    favorite_records = list(
        Favorite.objects.filter(
            user=request.user,
            cocktail__is_published=True,
        )
        .select_related(
            "cocktail",
            "cocktail__glassware",
        )
        .order_by("-created_at")
    )

    favorite_cocktails = [favorite.cocktail for favorite in favorite_records]

    learning_paths = list(
        LearningPath.objects.filter(
            is_published=True,
        ).order_by(
            "order",
            "title",
        )
    )

    published_lessons = list(
        Lesson.objects.filter(
            is_published=True,
            learning_path__is_published=True,
        )
        .select_related("learning_path")
        .order_by(
            "learning_path__order",
            "order",
            "title",
        )
    )

    progress_records = list(
        LessonProgress.objects.filter(
            user=request.user,
            lesson__is_published=True,
            lesson__learning_path__is_published=True,
        )
        .select_related(
            "lesson",
            "lesson__learning_path",
        )
        .order_by("-completed_at")
    )

    completed_lesson_ids = {
        progress.lesson.pk for progress in progress_records if progress.lesson.pk is not None
    }

    lessons_by_path: dict[int, list[Lesson]] = defaultdict(list)

    for lesson in published_lessons:
        path_id = lesson.learning_path.pk

        if path_id is not None:
            lessons_by_path[path_id].append(lesson)

    path_progress = []

    for learning_path in learning_paths:
        path_id = learning_path.pk

        if path_id is None:
            continue

        path_lessons = lessons_by_path.get(
            path_id,
            [],
        )

        completed_count = sum(1 for lesson in path_lessons if lesson.pk in completed_lesson_ids)

        total_count = len(path_lessons)

        progress_percentage = round(completed_count / total_count * 100) if total_count else 0

        next_lesson = next(
            (lesson for lesson in path_lessons if lesson.pk not in completed_lesson_ids),
            None,
        )

        path_progress.append(
            {
                "path": learning_path,
                "completed_count": completed_count,
                "total_count": total_count,
                "progress_percentage": progress_percentage,
                "next_lesson": next_lesson,
                "has_started": completed_count > 0,
                "is_completed": (total_count > 0 and completed_count == total_count),
            }
        )

    started_paths = [item for item in path_progress if item["has_started"]]

    next_lesson = next(
        (item["next_lesson"] for item in started_paths if item["next_lesson"] is not None),
        None,
    )

    if next_lesson is None:
        next_lesson = next(
            (item["next_lesson"] for item in path_progress if item["next_lesson"] is not None),
            None,
        )

    context = {
        "favorite_cocktails": favorite_cocktails,
        "favorite_count": len(favorite_cocktails),
        "completed_lesson_count": len(completed_lesson_ids),
        "started_paths": started_paths,
        "next_lesson": next_lesson,
        "recent_progress": progress_records[:5],
    }

    return render(
        request,
        "accounts/profile.html",
        context,
    )
