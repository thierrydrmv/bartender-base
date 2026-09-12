from django.template.defaultfilters import slugify
from django.test import TestCase
from django.urls import reverse

from cocktails.models import Cocktail, Glassware


class HomeViewTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.glassware = Glassware.objects.create(
            name="Coupe",
            description="Classic cocktail glass.",
        )

    @classmethod
    def create_cocktail(cls, name, is_published=True):
        return Cocktail.objects.create(
            name=name,
            slug=slugify(name),
            description=f"Description for {name}.",
            instructions=f"Instructions for {name}.",
            preparation_time=5,
            glassware=cls.glassware,
            is_published=is_published,
        )

    def test_home_returns_success(self):
        response = self.client.get(reverse("home"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "core/home.html")

    def test_home_displays_published_cocktails(self):
        published = self.create_cocktail("Published cocktail")
        unpublished = self.create_cocktail(
            "Unpublished cocktail",
            is_published=False,
        )

        response = self.client.get(reverse("home"))

        cocktails = response.context["cocktails"]

        self.assertIn(published, cocktails)
        self.assertNotIn(unpublished, cocktails)

    def test_home_displays_at_most_six_cocktails(self):
        for number in range(8):
            self.create_cocktail(f"Cocktail {number}")

        response = self.client.get(reverse("home"))

        cocktails = response.context["cocktails"]

        self.assertEqual(len(cocktails), 6)

    def test_home_orders_cocktails_by_most_recent(self):
        oldest = self.create_cocktail("Oldest cocktail")
        newest = self.create_cocktail("Newest cocktail")

        response = self.client.get(reverse("home"))

        cocktails = list(response.context["cocktails"])

        self.assertEqual(cocktails[0], newest)
        self.assertEqual(cocktails[1], oldest)
