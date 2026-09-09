from django.urls import path

from . import views

app_name = "cocktails"

urlpatterns = [
    path("", views.cocktail_list, name="list"),
    path(
        "what-can-i-make/",
        views.cocktail_matcher,
        name="matcher",
    ),
    path(
        "equipment/",
        views.equipment_list,
        name="equipment-list",
    ),
    path(
        "equipment/<slug:slug>/",
        views.equipment_detail,
        name="equipment-detail",
    ),
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
