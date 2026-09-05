from django.contrib import admin

from .models import (
    Cocktail,
    CocktailIngredient,
    Equipment,
    Glassware,
    Ingredient,
    IngredientCategory,
    Technique,
)


class CocktailIngredientInline(admin.TabularInline):
    model = CocktailIngredient
    extra = 1
    autocomplete_fields = ["ingredient"]


@admin.register(Cocktail)
class CocktailAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "difficulty",
        "is_alcoholic",
        "is_published",
        "updated_at",
    )
    list_filter = (
        "difficulty",
        "is_alcoholic",
        "is_published",
        "techniques",
    )
    search_fields = ("name", "description")
    prepopulated_fields = {"slug": ("name",)}
    filter_horizontal = ("techniques", "equipment")
    inlines = [CocktailIngredientInline]


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ("name", "category", "is_alcoholic")
    list_filter = ("category", "is_alcoholic")
    search_fields = ("name",)
    prepopulated_fields = {"slug": ("name",)}


@admin.register(IngredientCategory)
class IngredientCategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Technique)
class TechniqueAdmin(admin.ModelAdmin):
    search_fields = ("name",)
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Equipment)
class EquipmentAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Glassware)
class GlasswareAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}
