# Create your views here.
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from cocktails.models import Cocktail

from .forms import RegisterForm


def register(request):
    if request.user.is_authenticated:
        return redirect("accounts:profile")

    form = RegisterForm(
        request.POST or None,
    )

    if request.method == "POST" and form.is_valid():
        user = form.save()
        login(request, user)

        return redirect("accounts:profile")

    return render(
        request,
        "accounts/register.html",
        {"form": form},
    )


@login_required
def profile(request):
    favorite_cocktails = (
        Cocktail.objects.filter(
            favorites__user=request.user,
            is_published=True,
        )
        .select_related("glassware")
        .order_by("name")
    )

    context = {
        "favorite_cocktails": favorite_cocktails,
    }

    return render(
        request,
        "accounts/profile.html",
        context,
    )
