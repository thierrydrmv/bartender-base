# Create your views here.
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

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
    return render(
        request,
        "accounts/profile.html",
    )
