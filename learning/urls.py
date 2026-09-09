from django.urls import path

from . import views

app_name = "learning"

urlpatterns = [
    path(
        "",
        views.learning_path_list,
        name="path-list",
    ),
    path(
        "trilhas/<slug:slug>/",
        views.learning_path_detail,
        name="path-detail",
    ),
    path(
        "aulas/<slug:slug>/toggle-completion/",
        views.toggle_lesson_completion,
        name="toggle-completion",
    ),
    path(
        "aulas/<slug:slug>/",
        views.lesson_detail,
        name="lesson-detail",
    ),
]
