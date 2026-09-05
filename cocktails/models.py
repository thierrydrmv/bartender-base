from django.db import models
from django.urls import reverse


class IngredientCategory(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=120, unique=True)
    description = models.TextField(blank=True)

    class Meta:
        ordering = ["name"]
        verbose_name = "categoria de ingrediente"
        verbose_name_plural = "categorias de ingredientes"

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=120, unique=True)
    description = models.TextField(blank=True)
    category = models.ForeignKey(
        IngredientCategory,
        on_delete=models.PROTECT,
        related_name="ingredients",
    )
    image = models.ImageField(
        upload_to="ingredients/",
        blank=True,
    )
    is_alcoholic = models.BooleanField(
        default=False,
        verbose_name="contém álcool",
    )

    class Meta:
        ordering = ["name"]
        verbose_name = "ingrediente"
        verbose_name_plural = "ingredientes"

    def __str__(self):
        return self.name


class Technique(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=120, unique=True)
    description = models.TextField()
    instructions = models.TextField(blank=True)

    class Meta:
        ordering = ["name"]
        verbose_name = "técnica"
        verbose_name_plural = "técnicas"

    def __str__(self):
        return self.name


class Equipment(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=120, unique=True)
    description = models.TextField(blank=True)
    image = models.ImageField(
        upload_to="equipment/",
        blank=True,
    )

    class Meta:
        ordering = ["name"]
        verbose_name = "equipamento"
        verbose_name_plural = "equipamentos"

    def __str__(self):
        return self.name


class Glassware(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=120, unique=True)
    description = models.TextField(blank=True)
    image = models.ImageField(
        upload_to="glassware/",
        blank=True,
    )

    class Meta:
        ordering = ["name"]
        verbose_name = "tipo de copo"
        verbose_name_plural = "tipos de copo"

    def __str__(self):
        return self.name


class Cocktail(models.Model):
    class Difficulty(models.TextChoices):
        EASY = "easy", "Fácil"
        MEDIUM = "medium", "Intermediário"
        HARD = "hard", "Difícil"

    name = models.CharField(max_length=120, unique=True)
    slug = models.SlugField(max_length=140, unique=True)
    description = models.TextField()
    instructions = models.TextField(
        help_text="Descreva o preparo passo a passo.",
    )
    image = models.ImageField(
        upload_to="cocktails/",
        blank=True,
    )
    difficulty = models.CharField(
        max_length=10,
        choices=Difficulty.choices,
        default=Difficulty.EASY,
    )
    preparation_time = models.PositiveSmallIntegerField(
        default=5,
        help_text="Tempo estimado em minutos.",
    )
    glassware = models.ForeignKey(
        Glassware,
        on_delete=models.PROTECT,
        related_name="cocktails",
    )
    techniques = models.ManyToManyField(
        Technique,
        related_name="cocktails",
        blank=True,
    )
    equipment = models.ManyToManyField(
        Equipment,
        related_name="cocktails",
        blank=True,
    )
    ingredients = models.ManyToManyField(
        Ingredient,
        through="CocktailIngredient",
        related_name="cocktails",
    )
    garnish = models.CharField(
        max_length=150,
        blank=True,
        verbose_name="guarnição",
    )
    is_alcoholic = models.BooleanField(
        default=True,
        verbose_name="contém álcool",
    )
    is_published = models.BooleanField(
        default=False,
        verbose_name="publicado",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["name"]
        verbose_name = "drink"
        verbose_name_plural = "drinks"

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse(
            "cocktails:detail",
            kwargs={"slug": self.slug},
        )


class CocktailIngredient(models.Model):
    class Unit(models.TextChoices):
        MILLILITER = "ml", "ml"
        OUNCE = "oz", "oz"
        GRAM = "g", "g"
        UNIT = "unit", "unidade"
        DASH = "dash", "dash"
        BAR_SPOON = "bar_spoon", "colher bailarina"
        TO_TASTE = "to_taste", "a gosto"

    cocktail = models.ForeignKey(
        Cocktail,
        on_delete=models.CASCADE,
        related_name="ingredient_items",
    )
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.PROTECT,
        related_name="cocktail_items",
    )
    quantity = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        null=True,
        blank=True,
    )
    unit = models.CharField(
        max_length=20,
        choices=Unit.choices,
        default=Unit.MILLILITER,
    )
    notes = models.CharField(
        max_length=150,
        blank=True,
        help_text="Ex.: cortado em cubos ou recém-espremido.",
    )
    is_optional = models.BooleanField(
        default=False,
        verbose_name="opcional",
    )
    order = models.PositiveSmallIntegerField(default=0)

    class Meta:
        ordering = ["order", "id"]
        verbose_name = "ingrediente do drink"
        verbose_name_plural = "ingredientes do drink"
        constraints = [
            models.UniqueConstraint(
                fields=["cocktail", "ingredient"],
                name="unique_ingredient_per_cocktail",
            )
        ]

    def __str__(self):
        return f"{self.cocktail} — {self.ingredient}"
