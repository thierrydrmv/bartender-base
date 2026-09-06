from django.test import TestCase
from django.urls import reverse

from cocktails.models import (
    Cocktail,
    CocktailIngredient,
    Equipment,
    Glassware,
    Ingredient,
    IngredientCategory,
    Technique,
)


class CocktailModelTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.category = IngredientCategory.objects.create(
            name="Destilados",
            slug="destilados",
        )

        cls.ingredient = Ingredient.objects.create(
            name="Cachaça",
            slug="cachaca",
            category=cls.category,
            is_alcoholic=True,
        )

        cls.technique = Technique.objects.create(
            name="Montado",
            slug="montado",
            description="Preparado diretamente no copo.",
        )

        cls.equipment = Equipment.objects.create(
            name="Dosador",
            slug="dosador",
        )

        cls.glassware = Glassware.objects.create(
            name="Copo rocks",
            slug="copo-rocks",
        )

        cls.cocktail = Cocktail.objects.create(
            name="Caipirinha",
            slug="caipirinha",
            description="Clássico brasileiro.",
            instructions="Macere, adicione cachaça e gelo.",
            difficulty=Cocktail.Difficulty.EASY,
            preparation_time=5,
            glassware=cls.glassware,
            is_alcoholic=True,
            is_published=True,
        )

        cls.cocktail.techniques.add(cls.technique)
        cls.cocktail.equipment.add(cls.equipment)

        cls.cocktail_ingredient = CocktailIngredient.objects.create(
            cocktail=cls.cocktail,
            ingredient=cls.ingredient,
            quantity=60,
            unit=CocktailIngredient.Unit.MILLILITER,
            order=1,
        )

    def test_cocktail_string_representation(self):
        self.assertEqual(str(self.cocktail), "Caipirinha")

    def test_ingredient_string_representation(self):
        self.assertEqual(str(self.ingredient), "Cachaça")

    def test_cocktail_absolute_url(self):
        expected_url = reverse(
            "cocktails:detail",
            kwargs={"slug": "caipirinha"},
        )

        self.assertEqual(
            self.cocktail.get_absolute_url(),
            expected_url,
        )

    def test_cocktail_has_ingredient(self):
        self.assertTrue(
            self.cocktail.ingredients.filter(
                pk=self.ingredient.pk,
            ).exists()
        )

    def test_cocktail_has_technique(self):
        self.assertTrue(
            self.cocktail.techniques.filter(
                pk=self.technique.pk,
            ).exists()
        )

    def test_cocktail_has_equipment(self):
        self.assertTrue(
            self.cocktail.equipment.filter(
                pk=self.equipment.pk,
            ).exists()
        )

    def test_cocktail_ingredient_string_representation(self):
        self.assertEqual(
            str(self.cocktail_ingredient),
            "Caipirinha — Cachaça",
        )
