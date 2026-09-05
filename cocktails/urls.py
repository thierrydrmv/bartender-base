from django.urls import path

from . import views

app_name = "cocktails"

urlpatterns = [
    path(
        "ingredients/",
        views.ingredient_list,
        name="ingredient-list",
    ),
    path(
        "ingredients/<slug:slug>/",
        views.ingredient_detail,
        name="ingredient-detail",
    ),
    path(
        "techniques/",
        views.technique_list,
        name="technique-list",
    ),
    path(
        "techniques/<slug:slug>/",
        views.technique_detail,
        name="technique-detail",
    ),
    path(
        "<slug:slug>/",
        views.cocktail_detail,
        name="detail",
    ),
]
