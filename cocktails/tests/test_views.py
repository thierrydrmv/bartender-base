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


class CocktailViewTests(TestCase):
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

        cls.published_cocktail = Cocktail.objects.create(
            name="Caipirinha",
            slug="caipirinha",
            description="Drink brasileiro com limão.",
            instructions="Macere e misture.",
            difficulty=Cocktail.Difficulty.EASY,
            preparation_time=5,
            glassware=cls.glassware,
            is_alcoholic=True,
            is_published=True,
        )

        cls.published_cocktail.techniques.add(cls.technique)
        cls.published_cocktail.equipment.add(cls.equipment)

        CocktailIngredient.objects.create(
            cocktail=cls.published_cocktail,
            ingredient=cls.ingredient,
            quantity=60,
            unit=CocktailIngredient.Unit.MILLILITER,
        )

        cls.unpublished_cocktail = Cocktail.objects.create(
            name="Drink secreto",
            slug="drink-secreto",
            description="Ainda não publicado.",
            instructions="Conteúdo em construção.",
            difficulty=Cocktail.Difficulty.HARD,
            glassware=cls.glassware,
            is_published=False,
        )

    def test_cocktail_list_returns_success(self):
        response = self.client.get(
            reverse("cocktails:list"),
        )

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response,
            "cocktails/cocktail_list.html",
        )

    def test_list_displays_published_cocktail(self):
        response = self.client.get(
            reverse("cocktails:list"),
        )

        self.assertContains(response, "Caipirinha")

    def test_list_hides_unpublished_cocktail(self):
        response = self.client.get(
            reverse("cocktails:list"),
        )

        self.assertNotContains(response, "Drink secreto")

    def test_published_cocktail_detail_returns_success(self):
        response = self.client.get(
            self.published_cocktail.get_absolute_url(),
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Caipirinha")
        self.assertTemplateUsed(
            response,
            "cocktails/cocktail_detail.html",
        )

    def test_unpublished_cocktail_detail_returns_404(self):
        response = self.client.get(
            self.unpublished_cocktail.get_absolute_url(),
        )

        self.assertEqual(response.status_code, 404)

    def test_unknown_cocktail_returns_404(self):
        response = self.client.get(
            reverse(
                "cocktails:detail",
                kwargs={"slug": "nao-existe"},
            )
        )

        self.assertEqual(response.status_code, 404)

    def test_search_by_cocktail_name(self):
        response = self.client.get(
            reverse("cocktails:list"),
            {"q": "caipirinha"},
        )

        self.assertContains(response, "Caipirinha")
        self.assertNotContains(response, "Drink secreto")

    def test_search_by_ingredient(self):
        response = self.client.get(
            reverse("cocktails:list"),
            {"q": "cachaça"},
        )

        self.assertContains(response, "Caipirinha")

    def test_filter_by_difficulty(self):
        response = self.client.get(
            reverse("cocktails:list"),
            {"difficulty": Cocktail.Difficulty.EASY},
        )

        self.assertContains(response, "Caipirinha")

    def test_filter_by_technique(self):
        response = self.client.get(
            reverse("cocktails:list"),
            {"technique": self.technique.slug},
        )

        self.assertContains(response, "Caipirinha")

    def test_filter_by_alcoholic_type(self):
        response = self.client.get(
            reverse("cocktails:list"),
            {"type": "alcoholic"},
        )

        self.assertContains(response, "Caipirinha")

    def test_ingredient_detail_displays_related_cocktail(self):
        response = self.client.get(
            self.ingredient.get_absolute_url(),
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Caipirinha")

    def test_technique_detail_displays_related_cocktail(self):
        response = self.client.get(
            self.technique.get_absolute_url(),
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Caipirinha")

    def test_equipment_detail_displays_related_cocktail(self):
        response = self.client.get(
            self.equipment.get_absolute_url(),
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Caipirinha")
