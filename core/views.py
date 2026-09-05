from django.shortcuts import render

from cocktails.models import Cocktail


def home(request):
    cocktails = (
        Cocktail.objects.filter(is_published=True)
        .select_related("glassware")
        .prefetch_related("techniques")
        .order_by("-created_at")[:3]
    )

    context = {
        "cocktails": cocktails,
    }

    return render(request, "core/home.html", context)
