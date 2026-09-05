# Create your views here.
from django.shortcuts import get_object_or_404, render

from .models import Cocktail


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
