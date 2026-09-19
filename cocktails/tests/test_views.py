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


class CatalogListViewTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.category = IngredientCategory.objects.create(
            name="Spirits",
            slug="spirits",
        )
        cls.other_category = IngredientCategory.objects.create(
            name="Fruit",
            slug="fruit",
        )

        cls.ingredient = Ingredient.objects.create(
            name="Gin",
            slug="gin",
            description="A distilled spirit.",
            category=cls.category,
        )
        cls.other_ingredient = Ingredient.objects.create(
            name="Lemon",
            slug="lemon",
            description="A citrus fruit.",
            category=cls.other_category,
        )

        cls.technique = Technique.objects.create(
            name="Shake",
            slug="shake",
            description="Shake the ingredients with ice.",
        )
        cls.other_technique = Technique.objects.create(
            name="Stir",
            slug="stir",
            description="Stir the ingredients with ice.",
        )

        cls.equipment = Equipment.objects.create(
            name="Shaker",
            slug="shaker",
            description="Used to shake cocktails.",
        )
        cls.other_equipment = Equipment.objects.create(
            name="Bar spoon",
            slug="bar-spoon",
            description="Used to stir cocktails.",
        )

        cls.glassware = Glassware.objects.create(
            name="Coupe",
            slug="coupe",
            description="Classic cocktail glass.",
        )

        cls.non_alcoholic_cocktail = Cocktail.objects.create(
            name="Citrus Cooler",
            slug="citrus-cooler",
            description="A non-alcoholic citrus drink.",
            instructions="Build over ice.",
            preparation_time=5,
            glassware=cls.glassware,
            is_alcoholic=False,
            is_published=True,
        )

        cls.alcoholic_cocktail = Cocktail.objects.create(
            name="Gin Cocktail",
            slug="gin-cocktail",
            description="A cocktail made with gin.",
            instructions="Shake and strain.",
            preparation_time=5,
            glassware=cls.glassware,
            is_alcoholic=True,
            is_published=True,
        )

    def test_cocktail_list_filters_non_alcoholic_drinks(self):
        response = self.client.get(
            reverse("cocktails:list"),
            {"type": "non_alcoholic"},
        )

        cocktails = response.context["page"].object_list

        self.assertIn(self.non_alcoholic_cocktail, cocktails)
        self.assertNotIn(self.alcoholic_cocktail, cocktails)
        self.assertEqual(
            response.context["selected_type"],
            "non_alcoholic",
        )

    def test_ingredient_list_returns_success(self):
        response = self.client.get(
            reverse("cocktails:ingredient-list"),
        )

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response,
            "cocktails/ingredient_list.html",
        )
        self.assertContains(response, self.ingredient.name)

    def test_ingredient_list_searches_by_name(self):
        response = self.client.get(
            reverse("cocktails:ingredient-list"),
            {"q": "Gin"},
        )

        ingredients = response.context["page"].object_list

        self.assertIn(self.ingredient, ingredients)
        self.assertNotIn(self.other_ingredient, ingredients)
        self.assertEqual(response.context["query"], "Gin")

    def test_ingredient_list_filters_by_category(self):
        response = self.client.get(
            reverse("cocktails:ingredient-list"),
            {"category": self.category.slug},
        )

        ingredients = response.context["page"].object_list

        self.assertIn(self.ingredient, ingredients)
        self.assertNotIn(self.other_ingredient, ingredients)
        self.assertEqual(
            response.context["selected_category"],
            self.category.slug,
        )

    def test_technique_list_returns_success(self):
        response = self.client.get(
            reverse("cocktails:technique-list"),
        )

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response,
            "cocktails/technique_list.html",
        )

    def test_technique_list_searches_by_name(self):
        response = self.client.get(
            reverse("cocktails:technique-list"),
            {"q": "Shake"},
        )

        techniques = response.context["page"].object_list

        self.assertIn(self.technique, techniques)
        self.assertNotIn(self.other_technique, techniques)
        self.assertEqual(response.context["query"], "Shake")

    def test_equipment_list_returns_success(self):
        response = self.client.get(
            reverse("cocktails:equipment-list"),
        )

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response,
            "cocktails/equipment_list.html",
        )

    def test_equipment_list_searches_by_name(self):
        response = self.client.get(
            reverse("cocktails:equipment-list"),
            {"q": "Shaker"},
        )

        equipment = response.context["page"].object_list

        self.assertIn(self.equipment, equipment)
        self.assertNotIn(self.other_equipment, equipment)
        self.assertEqual(response.context["query"], "Shaker")

    def test_matcher_ignores_cocktail_without_required_ingredients(self):
        response = self.client.get(
            reverse("cocktails:matcher"),
            {"ingredients": self.ingredient.pk},
        )

        self.assertTrue(response.context["has_selection"])
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


class GlasswareListTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.coupe = Glassware.objects.create(
            name="Taça coupe",
            slug="taca-coupe",
            description="Taça de haste com bojo largo e raso.",
        )

        cls.highball = Glassware.objects.create(
            name="Copo highball",
            slug="copo-highball",
            description="Copo alto utilizado em drinks refrescantes.",
        )

        cls.old_fashioned = Glassware.objects.create(
            name="Copo old fashioned",
            slug="copo-old-fashioned",
            description="Copo baixo e resistente.",
        )

    def test_glassware_list_returns_success(self):
        response = self.client.get(
            reverse("cocktails:glassware-list"),
        )

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response,
            "cocktails/glassware_list.html",
        )

    def test_glassware_list_displays_glassware(self):
        response = self.client.get(
            reverse("cocktails:glassware-list"),
        )

        self.assertContains(response, self.coupe.name)
        self.assertContains(response, self.highball.name)
        self.assertContains(response, self.old_fashioned.name)

    def test_glassware_are_ordered_by_name(self):
        response = self.client.get(
            reverse("cocktails:glassware-list"),
        )

        glassware = list(response.context["page"].object_list)

        self.assertEqual(
            glassware,
            [
                self.highball,
                self.old_fashioned,
                self.coupe,
            ],
        )

    def test_search_filters_glassware_by_name(self):
        response = self.client.get(
            reverse("cocktails:glassware-list"),
            {"q": "highball"},
        )

        page = response.context["page"]

        self.assertEqual(list(page.object_list), [self.highball])
        self.assertContains(response, self.highball.name)
        self.assertNotContains(response, self.coupe.name)

    def test_search_filters_glassware_by_description(self):
        response = self.client.get(
            reverse("cocktails:glassware-list"),
            {"q": "raso"},
        )

        page = response.context["page"]

        self.assertEqual(list(page.object_list), [self.coupe])

    def test_search_is_case_insensitive(self):
        response = self.client.get(
            reverse("cocktails:glassware-list"),
            {"q": "HIGHBALL"},
        )

        page = response.context["page"]

        self.assertEqual(list(page.object_list), [self.highball])

    def test_search_removes_surrounding_whitespace(self):
        response = self.client.get(
            reverse("cocktails:glassware-list"),
            {"q": "  highball  "},
        )

        self.assertEqual(
            response.context["query"],
            "highball",
        )
        self.assertEqual(
            list(response.context["page"].object_list),
            [self.highball],
        )

    def test_search_with_no_match_returns_empty_page(self):
        response = self.client.get(
            reverse("cocktails:glassware-list"),
            {"q": "inexistente"},
        )

        self.assertEqual(
            list(response.context["page"].object_list),
            [],
        )
        self.assertContains(
            response,
            "Nenhum copo encontrado.",
        )

    def test_glassware_list_paginates_nine_items(self):
        Glassware.objects.bulk_create(
            [
                Glassware(
                    name=f"Copo {number:02}",
                    slug=f"copo-{number:02}",
                    description="Descrição do copo.",
                )
                for number in range(10)
            ]
        )

        response = self.client.get(
            reverse("cocktails:glassware-list"),
        )

        page = response.context["page"]

        self.assertEqual(len(page.object_list), 9)
        self.assertTrue(page.has_next())

    def test_glassware_list_returns_second_page(self):
        Glassware.objects.bulk_create(
            [
                Glassware(
                    name=f"Copo {number:02}",
                    slug=f"copo-{number:02}",
                    description="Descrição do copo.",
                )
                for number in range(10)
            ]
        )

        response = self.client.get(
            reverse("cocktails:glassware-list"),
            {"page": 2},
        )

        page = response.context["page"]

        self.assertEqual(page.number, 2)
        self.assertTrue(page.has_previous())


class GlasswareDetailTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.glassware = Glassware.objects.create(
            name="Taça coupe",
            slug="taca-coupe",
            description="Taça de haste com bojo largo e raso.",
        )

        cls.other_glassware = Glassware.objects.create(
            name="Copo highball",
            slug="copo-highball",
            description="Copo alto utilizado em long drinks.",
        )

        cls.published_cocktail = Cocktail.objects.create(
            name="Daiquiri",
            slug="daiquiri",
            description="Cocktail clássico preparado com rum.",
            instructions="Bata os ingredientes com gelo.",
            difficulty="easy",
            preparation_time=5,
            glassware=cls.glassware,
            is_published=True,
        )

        cls.unpublished_cocktail = Cocktail.objects.create(
            name="Cocktail não publicado",
            slug="cocktail-nao-publicado",
            description="Receita ainda não publicada.",
            instructions="Misture os ingredientes.",
            difficulty="easy",
            preparation_time=5,
            glassware=cls.glassware,
            is_published=False,
        )

        cls.other_cocktail = Cocktail.objects.create(
            name="Gin Tônica",
            slug="gin-tonica",
            description="Cocktail servido em outro copo.",
            instructions="Monte diretamente no copo.",
            difficulty="easy",
            preparation_time=5,
            glassware=cls.other_glassware,
            is_published=True,
        )

    def test_glassware_detail_returns_success(self):
        response = self.client.get(
            reverse(
                "cocktails:glassware-detail",
                args=[self.glassware.slug],
            )
        )

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response,
            "cocktails/glassware_detail.html",
        )

    def test_glassware_detail_adds_glassware_to_context(self):
        response = self.client.get(
            reverse(
                "cocktails:glassware-detail",
                args=[self.glassware.slug],
            )
        )

        self.assertEqual(
            response.context["glassware"],
            self.glassware,
        )

    def test_glassware_detail_displays_published_cocktails(self):
        response = self.client.get(
            reverse(
                "cocktails:glassware-detail",
                args=[self.glassware.slug],
            )
        )

        cocktails = list(response.context["cocktails"])

        self.assertEqual(
            cocktails,
            [self.published_cocktail],
        )
        self.assertContains(
            response,
            self.published_cocktail.name,
        )

    def test_glassware_detail_excludes_unpublished_cocktails(self):
        response = self.client.get(
            reverse(
                "cocktails:glassware-detail",
                args=[self.glassware.slug],
            )
        )

        self.assertNotContains(
            response,
            self.unpublished_cocktail.name,
        )

    def test_glassware_detail_excludes_cocktails_from_other_glassware(self):
        response = self.client.get(
            reverse(
                "cocktails:glassware-detail",
                args=[self.glassware.slug],
            )
        )

        self.assertNotContains(
            response,
            self.other_cocktail.name,
        )

    def test_glassware_detail_returns_404_for_unknown_slug(self):
        response = self.client.get(
            reverse(
                "cocktails:glassware-detail",
                args=["copo-inexistente"],
            )
        )

        self.assertEqual(response.status_code, 404)
