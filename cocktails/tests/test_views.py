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


class CocktailMatcherTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.category = IngredientCategory.objects.create(
            name="Ingredientes do matcher",
            slug="ingredientes-do-matcher",
            description="Categoria utilizada nos testes.",
        )

        cls.rum = Ingredient.objects.create(
            name="Rum de teste",
            slug="rum-de-teste",
            category=cls.category,
            is_alcoholic=True,
        )

        cls.lime = Ingredient.objects.create(
            name="Limão de teste",
            slug="limao-de-teste",
            category=cls.category,
            is_alcoholic=False,
        )

        cls.syrup = Ingredient.objects.create(
            name="Xarope de teste",
            slug="xarope-de-teste",
            category=cls.category,
            is_alcoholic=False,
        )

        cls.mint = Ingredient.objects.create(
            name="Hortelã de teste",
            slug="hortela-de-teste",
            category=cls.category,
            is_alcoholic=False,
        )

        cls.glassware = Glassware.objects.create(
            name="Copo do matcher",
            slug="copo-do-matcher",
        )

        cls.cocktail = Cocktail.objects.create(
            name="Cocktail do matcher",
            slug="cocktail-do-matcher",
            description="Cocktail utilizado nos testes do matcher.",
            instructions="Misture todos os ingredientes.",
            difficulty=Cocktail.Difficulty.EASY,
            preparation_time=5,
            glassware=cls.glassware,
            is_alcoholic=True,
            is_published=True,
        )

        CocktailIngredient.objects.create(
            cocktail=cls.cocktail,
            ingredient=cls.rum,
            quantity=50,
            unit=CocktailIngredient.Unit.MILLILITER,
            order=1,
        )

        CocktailIngredient.objects.create(
            cocktail=cls.cocktail,
            ingredient=cls.lime,
            quantity=25,
            unit=CocktailIngredient.Unit.MILLILITER,
            order=2,
        )

        CocktailIngredient.objects.create(
            cocktail=cls.cocktail,
            ingredient=cls.syrup,
            quantity=15,
            unit=CocktailIngredient.Unit.MILLILITER,
            order=3,
        )

        CocktailIngredient.objects.create(
            cocktail=cls.cocktail,
            ingredient=cls.mint,
            quantity=5,
            unit=CocktailIngredient.Unit.UNIT,
            is_optional=True,
            order=4,
        )

        cls.unpublished_cocktail = Cocktail.objects.create(
            name="Cocktail não publicado",
            slug="cocktail-nao-publicado",
            description="Este cocktail não deve aparecer.",
            instructions="Receita não publicada.",
            difficulty=Cocktail.Difficulty.EASY,
            preparation_time=5,
            glassware=cls.glassware,
            is_alcoholic=True,
            is_published=False,
        )

        CocktailIngredient.objects.create(
            cocktail=cls.unpublished_cocktail,
            ingredient=cls.rum,
            quantity=50,
            unit=CocktailIngredient.Unit.MILLILITER,
        )

    def test_matcher_page_returns_success(self):
        response = self.client.get(
            reverse("cocktails:matcher"),
        )

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response,
            "cocktails/cocktail_matcher.html",
        )

    def test_matcher_displays_available_ingredients(self):
        response = self.client.get(
            reverse("cocktails:matcher"),
        )

        self.assertContains(response, self.rum.name)
        self.assertContains(response, self.lime.name)
        self.assertContains(response, self.syrup.name)
        self.assertContains(response, self.mint.name)

    def test_no_selection_does_not_calculate_results(self):
        response = self.client.get(
            reverse("cocktails:matcher"),
        )

        self.assertFalse(response.context["has_selection"])
        self.assertEqual(
            response.context["available_cocktails"],
            [],
        )
        self.assertEqual(
            response.context["missing_one_cocktails"],
            [],
        )
        self.assertEqual(
            response.context["missing_many_cocktails"],
            [],
        )

    def test_cocktail_is_available_with_all_required_ingredients(
        self,
    ):
        response = self.client.get(
            reverse("cocktails:matcher"),
            {
                "ingredients": [
                    self.rum.pk,
                    self.lime.pk,
                    self.syrup.pk,
                ]
            },
        )

        available = response.context["available_cocktails"]

        self.assertTrue(response.context["has_selection"])
        self.assertEqual(len(available), 1)
        self.assertEqual(
            available[0]["cocktail"],
            self.cocktail,
        )
        self.assertEqual(
            available[0]["missing_ingredients"],
            [],
        )

    def test_optional_ingredient_is_not_required(self):
        response = self.client.get(
            reverse("cocktails:matcher"),
            {
                "ingredients": [
                    self.rum.pk,
                    self.lime.pk,
                    self.syrup.pk,
                ]
            },
        )

        available = response.context["available_cocktails"]

        self.assertEqual(len(available), 1)
        self.assertEqual(
            available[0]["cocktail"],
            self.cocktail,
        )
        self.assertNotIn(
            self.mint,
            available[0]["missing_ingredients"],
        )

    def test_cocktail_appears_when_one_ingredient_is_missing(
        self,
    ):
        response = self.client.get(
            reverse("cocktails:matcher"),
            {
                "ingredients": [
                    self.rum.pk,
                    self.lime.pk,
                ]
            },
        )

        results = response.context["missing_one_cocktails"]

        self.assertEqual(len(results), 1)
        self.assertEqual(
            results[0]["cocktail"],
            self.cocktail,
        )
        self.assertEqual(
            results[0]["missing_count"],
            1,
        )
        self.assertEqual(
            results[0]["missing_ingredients"],
            [self.syrup],
        )

    def test_cocktail_appears_when_multiple_ingredients_are_missing(
        self,
    ):
        response = self.client.get(
            reverse("cocktails:matcher"),
            {
                "ingredients": [self.rum.pk],
            },
        )

        results = response.context["missing_many_cocktails"]

        self.assertEqual(len(results), 1)
        self.assertEqual(
            results[0]["cocktail"],
            self.cocktail,
        )
        self.assertEqual(
            results[0]["missing_count"],
            2,
        )
        self.assertCountEqual(
            results[0]["missing_ingredients"],
            [
                self.lime,
                self.syrup,
            ],
        )

    def test_unpublished_cocktail_is_not_in_results(self):
        response = self.client.get(
            reverse("cocktails:matcher"),
            {
                "ingredients": [
                    self.rum.pk,
                    self.lime.pk,
                    self.syrup.pk,
                ]
            },
        )

        all_results = [
            *response.context["available_cocktails"],
            *response.context["missing_one_cocktails"],
            *response.context["missing_many_cocktails"],
        ]

        result_cocktails = [result["cocktail"] for result in all_results]

        self.assertNotIn(
            self.unpublished_cocktail,
            result_cocktails,
        )

    def test_invalid_values_are_ignored(self):
        response = self.client.get(
            reverse("cocktails:matcher"),
            {
                "ingredients": [
                    "invalid",
                    "not-a-number",
                ]
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.context["has_selection"])

    def test_nonexistent_ids_are_ignored(self):
        response = self.client.get(
            reverse("cocktails:matcher"),
            {
                "ingredients": ["999999"],
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.context["has_selection"])

    def test_duplicate_ids_do_not_change_result(self):
        response = self.client.get(
            reverse("cocktails:matcher"),
            {
                "ingredients": [
                    self.rum.pk,
                    self.rum.pk,
                    self.lime.pk,
                    self.syrup.pk,
                ]
            },
        )

        available = response.context["available_cocktails"]

        self.assertEqual(len(available), 1)
        self.assertEqual(
            available[0]["cocktail"],
            self.cocktail,
        )

    def test_selected_ingredients_remain_checked(self):
        response = self.client.get(
            reverse("cocktails:matcher"),
            {
                "ingredients": [
                    self.rum.pk,
                    self.lime.pk,
                ]
            },
        )

        selected_ids = response.context["selected_ids"]

        self.assertEqual(
            selected_ids,
            {
                self.rum.pk,
                self.lime.pk,
            },
        )

    def test_available_result_contains_cocktail_link(self):
        response = self.client.get(
            reverse("cocktails:matcher"),
            {
                "ingredients": [
                    self.rum.pk,
                    self.lime.pk,
                    self.syrup.pk,
                ]
            },
        )

        self.assertContains(
            response,
            self.cocktail.get_absolute_url(),
        )

    def test_missing_ingredient_contains_detail_link(self):
        response = self.client.get(
            reverse("cocktails:matcher"),
            {
                "ingredients": [
                    self.rum.pk,
                    self.lime.pk,
                ]
            },
        )

        self.assertContains(
            response,
            self.syrup.get_absolute_url(),
        )

    def test_form_points_to_results_anchor(self):
        response = self.client.get(
            reverse("cocktails:matcher"),
        )

        expected_action = f"{reverse('cocktails:matcher')}#results"

        self.assertContains(
            response,
            f'action="{expected_action}"',
        )

    def test_missing_many_requires_at_least_one_required_ingredient(
        self,
    ):
        response = self.client.get(
            reverse("cocktails:matcher"),
            {
                "ingredients": [self.mint.pk],
            },
        )

        self.assertTrue(response.context["has_selection"])
        self.assertEqual(
            response.context["missing_many_cocktails"],
            [],
        )
