from django.db import models


class Ingredient(models.Model):
    """Ингредиенты."""

    pass


class Tag(models.Model):
    """Тэги."""

    pass


class Recipe(models.Model):
    """Рецепты."""

    pass


class RecipesFavorite(models.Model):
    """Избранные рецепты."""

    pass


class ShoppingCart(models.Model):
    """Список покупок."""

    pass


class Follow(models.Model):
    """Подписки на авторов рецептов."""

    pass
