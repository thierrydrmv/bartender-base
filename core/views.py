from django.shortcuts import render

from cocktails.models import Cocktail, Ingredient


def home(request):
    cocktails = (
        Cocktail.objects.filter(is_published=True)
        .select_related("glassware")
        .prefetch_related("techniques")
        .order_by("-created_at")[:6]
    )
    featured_slugs = [
        "limao-taiti",
        "vodka",
        "hortela",
        "acucar",
        "cachaca",
    ]

    featured_ingredients = Ingredient.objects.filter(
        slug__in=featured_slugs,
    )

    context = {
        "cocktails": cocktails,
        "featured_ingredients": featured_ingredients,
    }

    return render(request, "core/home.html", context)
