# Create your views here.
from django.db.models import Q
from django.shortcuts import get_object_or_404, render

from .models import Cocktail, Ingredient, IngredientCategory, Technique


def cocktail_detail(request, slug):
    cocktail = get_object_or_404(
        Cocktail.objects.select_related("glassware").prefetch_related(
            "techniques",
            "equipment",
            "ingredient_items__ingredient",
        ),
        slug=slug,
        is_published=True,
    )

    context = {
        "cocktail": cocktail,
    }

    return render(request, "cocktails/cocktail_detail.html", context)


def ingredient_list(request):
    query = request.GET.get("q", "").strip()
    category_slug = request.GET.get("category", "").strip()

    ingredients = Ingredient.objects.select_related("category")

    if query:
        ingredients = ingredients.filter(
            Q(name__icontains=query)
            | Q(description__icontains=query)
            | Q(category__name__icontains=query)
        )

    if category_slug:
        ingredients = ingredients.filter(category__slug=category_slug)

    context = {
        "ingredients": ingredients,
        "categories": IngredientCategory.objects.all(),
        "query": query,
        "selected_category": category_slug,
    }

    return render(request, "cocktails/ingredient_list.html", context)


def ingredient_detail(request, slug):
    ingredient = get_object_or_404(
        Ingredient.objects.select_related("category"),
        slug=slug,
    )

    cocktails = Cocktail.objects.filter(
        ingredients=ingredient,
        is_published=True,
    )

    context = {
        "ingredient": ingredient,
        "cocktails": cocktails,
    }

    return render(request, "cocktails/ingredient_detail.html", context)


def technique_list(request):
    query = request.GET.get("q", "").strip()

    techniques = Technique.objects.all()

    if query:
        techniques = techniques.filter(Q(name__icontains=query) | Q(description__icontains=query))

    context = {
        "techniques": techniques,
        "query": query,
    }

    return render(request, "cocktails/technique_list.html", context)


def technique_detail(request, slug):
    technique = get_object_or_404(
        Technique.objects.prefetch_related("cocktails"),
        slug=slug,
    )

    cocktails = Cocktail.objects.filter(
        techniques=technique,
        is_published=True,
    )

    context = {
        "technique": technique,
        "cocktails": cocktails,
    }

    return render(request, "cocktails/technique_detail.html", context)
