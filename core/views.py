from django.shortcuts import render

from cocktails.models import Cocktail, Ingredient


def home(request):
    cocktails = (
        Cocktail.objects.filter(is_published=True)
        .select_related("glassware")
        .prefetch_related("techniques")
        .order_by("-created_at")[:6]
    )
    featured_names = [
        "Limão",
        "Vodka",
        "Hortelã",
        "Açúcar",
        "Cachaça",
    ]

    featured_ingredients = Ingredient.objects.filter(
        name__in=featured_names,
    )

    context = {
        "cocktails": cocktails,
        "featured_ingredients": featured_ingredients,
    }

    return render(request, "core/home.html", context)
