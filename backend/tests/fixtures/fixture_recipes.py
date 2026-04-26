"""Fixtures for recipes, tags and ingredients."""
import pytest


@pytest.fixture
def tag(db):
    """Создание тега 'Завтрак'."""
    from recipes.models import Tag
    obj, _ = Tag.objects.get_or_create(
        slug='breakfast',
        defaults={
            'name': 'Завтрак',
            'color': '#FF0000',
        }
    )
    return obj


@pytest.fixture
def tag2(db):
    """Создание тега 'Ужин'."""
    from recipes.models import Tag
    obj, _ = Tag.objects.get_or_create(
        slug='dinner',
        defaults={
            'name': 'Ужин',
            'color': '#00FF00',
        }
    )
    return obj


@pytest.fixture
def ingredient(db):
    """Создание ингредиента 'Яйцо'."""
    from recipes.models import Ingredient
    obj, _ = Ingredient.objects.get_or_create(
        name='Яйцо',
        measurement_unit='шт'
    )
    return obj


@pytest.fixture
def ingredient2(db):
    """Создание ингредиента 'Молоко'."""
    from recipes.models import Ingredient
    obj, _ = Ingredient.objects.get_or_create(
        name='Молоко',
        measurement_unit='мл'
    )
    return obj


@pytest.fixture
def ingredient_salt(db):
    """Создание ингредиента 'Соль'."""
    from recipes.models import Ingredient
    obj, _ = Ingredient.objects.get_or_create(
        name='Соль',
        measurement_unit='г'
    )
    return obj


@pytest.fixture
def recipe(db, user, tag, ingredient):
    """Создание тестового рецепта 'Омлет'."""
    from recipes.models import IngredientInRecipe, Recipe
    b64 = 'iVBORw0KGgoAAAANSUhEUgAAAAoAAAAKCAYAAACNMs+9AAAAGElEQVR4nGP8'
    b64 += 'z8Dwn4EIwESMolGF1FMIAD2cAhK2AyPVAAAAAElFTkSuQmCC'
    recipe = Recipe.objects.create(
        author=user,
        name='Омлет',
        text='Взбить яйца и пожарить на сковороде',
        cooking_time=15,
        image=f'data:image/png;base64,{b64}',
    )
    recipe.tags.add(tag)
    IngredientInRecipe.objects.create(
        recipe=recipe,
        ingredient=ingredient,
        amount=2
    )
    return recipe


@pytest.fixture
def recipe2(db, user2, tag2, ingredient2, recipe):
    """Создание второго тестового рецепта 'Молочная каша'."""
    from recipes.models import IngredientInRecipe, Recipe
    b64 = 'iVBORw0KGgoAAAANSUhEUgAAAAoAAAAKCAYAAACNMs+9AAAAGElEQVR4nGP8'
    b64 += 'z8Dwn4EIwESMolGF1FMIAD2cAhK2AyPVAAAAAElFTkSuQmCC'
    recipe = Recipe.objects.create(
        author=user2,
        name='Молочная каша',
        text='Сварить на молоке',
        cooking_time=20,
        image=f'data:image/png;base64,{b64}',
    )
    recipe.tags.add(tag2)
    IngredientInRecipe.objects.create(
        recipe=recipe,
        ingredient=ingredient2,
        amount=500
    )
    return recipe
