# Create your views here.
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from .models import (
    Cocktail,
    CocktailIngredient,
    Equipment,
    Favorite,
    Glassware,
    Ingredient,
    IngredientCategory,
    Technique,
)


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
    is_favorite = False

    if request.user.is_authenticated:
        is_favorite = Favorite.objects.filter(
            user=request.user,
            cocktail=cocktail,
        ).exists()

    context = {
        "cocktail": cocktail,
        "is_favorite": is_favorite,
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


def cocktail_matcher(request):
    selected_values = request.GET.getlist("ingredients")

    requested_ids: set[int] = {int(value) for value in selected_values if value.isdigit()}

    ingredients = Ingredient.objects.select_related("category").order_by(
        "category__name",
        "name",
    )

    selected_ingredients = ingredients.filter(
        pk__in=requested_ids,
    )

    selected_ids: set[int] = set(
        selected_ingredients.values_list(
            "pk",
            flat=True,
        )
    )

    has_selection = bool(selected_ids)

    available_cocktails = []
    missing_one_cocktails = []
    missing_many_cocktails = []

    if has_selection:
        cocktails = list(
            Cocktail.objects.filter(
                is_published=True,
            )
            .select_related("glassware")
            .prefetch_related("techniques")
            .order_by("name")
        )

        required_items = (
            CocktailIngredient.objects.filter(
                cocktail__in=cocktails,
                is_optional=False,
            )
            .select_related(
                "cocktail",
                "ingredient",
            )
            .order_by(
                "cocktail__name",
                "order",
            )
        )

        required_items_by_cocktail: dict[
            int,
            list[CocktailIngredient],
        ] = {}

        for item in required_items:
            cocktail_id = item.cocktail.pk

            if cocktail_id is None:
                continue

            required_items_by_cocktail.setdefault(
                cocktail_id,
                [],
            ).append(item)

        for cocktail in cocktails:
            cocktail_id = cocktail.pk

            if cocktail_id is None:
                continue

            cocktail_required_items = required_items_by_cocktail.get(
                cocktail_id,
                [],
            )

            # Impede que cocktails sem ingredientes obrigatórios
            # sejam classificados como disponíveis.
            if not cocktail_required_items:
                continue

            required_ingredient_ids = {
                item.ingredient.pk
                for item in cocktail_required_items
                if item.ingredient.pk is not None
            }

            matched_ingredient_count = len(required_ingredient_ids & selected_ids)

            missing_ingredients = [
                item.ingredient
                for item in cocktail_required_items
                if item.ingredient.pk not in selected_ids
            ]

            result = {
                "cocktail": cocktail,
                "missing_ingredients": missing_ingredients,
                "missing_count": len(missing_ingredients),
                "matched_count": matched_ingredient_count,
            }

            if not missing_ingredients:
                available_cocktails.append(result)
            elif len(missing_ingredients) == 1:
                missing_one_cocktails.append(result)
            elif matched_ingredient_count >= 1:
                missing_many_cocktails.append(result)

        missing_many_cocktails.sort(key=lambda result: result["missing_count"])

    context = {
        "ingredients": ingredients,
        "selected_ids": selected_ids,
        "selected_ingredients": selected_ingredients,
        "has_selection": has_selection,
        "available_cocktails": available_cocktails,
        "missing_one_cocktails": missing_one_cocktails,
        "missing_many_cocktails": missing_many_cocktails,
    }

    return render(
        request,
        "cocktails/cocktail_matcher.html",
        context,
    )


@login_required
@require_POST
def toggle_favorite(request, slug):
    cocktail = get_object_or_404(
        Cocktail,
        slug=slug,
        is_published=True,
    )

    favorite, created = Favorite.objects.get_or_create(
        user=request.user,
        cocktail=cocktail,
    )

    if created:
        messages.success(
            request,
            f"{cocktail.name} foi adicionado aos favoritos.",
        )
    else:
        favorite.delete()

        messages.success(
            request,
            f"{cocktail.name} foi removido dos favoritos.",
        )

    return redirect(
        cocktail.get_absolute_url(),
    )


def glassware_list(request):
    query = request.GET.get("q", "").strip()

    glassware = Glassware.objects.all().order_by("name")

    if query:
        glassware = glassware.filter(Q(name__icontains=query) | Q(description__icontains=query))

    paginator = Paginator(glassware, 9)
    page = paginator.get_page(request.GET.get("page"))

    context = {
        "page": page,
        "query": query,
    }

    return render(
        request,
        "cocktails/glassware_list.html",
        context,
    )


def glassware_detail(request, slug):
    glassware = get_object_or_404(
        Glassware,
        slug=slug,
    )

    cocktails = (
        Cocktail.objects.filter(
            glassware=glassware,
            is_published=True,
        )
        .select_related("glassware")
        .order_by("name")
    )

    context = {
        "glassware": glassware,
        "cocktails": cocktails,
    }

    return render(
        request,
        "cocktails/glassware_detail.html",
        context,
    )
