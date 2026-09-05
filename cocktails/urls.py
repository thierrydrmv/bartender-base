from django.urls import path

from . import views

app_name = "cocktails"

urlpatterns = [
    path("<slug:slug>/", views.cocktail_detail, name="detail"),
]
