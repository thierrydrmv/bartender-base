# Create your views here.
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import get_object_or_404, render

from .models import Cocktail, Equipment, Ingredient, IngredientCategory, Technique


def cocktail_list(request):
    query = request.GET.get("q", "").strip()
    difficulty = request.GET.get("difficulty", "").strip()
    technique_slug = request.GET.get("technique", "").strip()
    drink_type = request.GET.get("type", "").strip()

    cocktails = (
        Cocktail.objects.filter(is_published=True)
        .select_related("glassware")
        .prefetch_related("techniques")
    )

    if query:
        cocktails = cocktails.filter(
            Q(name__icontains=query)
            | Q(description__icontains=query)
            | Q(ingredients__name__icontains=query)
        )

    if difficulty:
        cocktails = cocktails.filter(difficulty=difficulty)

    if technique_slug:
        cocktails = cocktails.filter(techniques__slug=technique_slug)

    if drink_type == "alcoholic":
        cocktails = cocktails.filter(is_alcoholic=True)
    elif drink_type == "non_alcoholic":
        cocktails = cocktails.filter(is_alcoholic=False)

    cocktails = cocktails.distinct().order_by("name")

    paginator = Paginator(cocktails, 9)
    page = paginator.get_page(request.GET.get("page"))

    context = {
        "page": page,
        "techniques": Technique.objects.all(),
        "difficulty_choices": Cocktail.Difficulty.choices,
        "query": query,
        "selected_difficulty": difficulty,
        "selected_technique": technique_slug,
        "selected_type": drink_type,
    }

    return render(
        request,
        "cocktails/cocktail_list.html",
        context,
    )


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

    paginator = Paginator(ingredients, 9)
    page = paginator.get_page(request.GET.get("page"))

    context = {
        "page": page,
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

    paginator = Paginator(techniques, 9)
    page = paginator.get_page(request.GET.get("page"))

    context = {
        "page": page,
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


def equipment_list(request):
    query = request.GET.get("q", "").strip()

    equipment = Equipment.objects.all()

    if query:
        equipment = equipment.filter(Q(name__icontains=query) | Q(description__icontains=query))

    paginator = Paginator(equipment, 9)
    page = paginator.get_page(request.GET.get("page"))

    context = {
        "page": page,
        "equipment": equipment,
        "query": query,
    }

    return render(
        request,
        "cocktails/equipment_list.html",
        context,
    )


def equipment_detail(request, slug):
    equipment = get_object_or_404(
        Equipment,
        slug=slug,
    )

    cocktails = Cocktail.objects.filter(
        equipment=equipment,
        is_published=True,
    )

    context = {
        "equipment": equipment,
        "cocktails": cocktails,
    }

    return render(
        request,
        "cocktails/equipment_detail.html",
        context,
    )
