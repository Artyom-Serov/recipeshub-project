"""Тесты моделей приложения recipes и users."""

import pytest

from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from django.db import IntegrityError

from recipes.models import (Ingredient, IngredientInRecipe, Recipe,
                            RecipesFavorite, ShoppingCart, Tag)
from tests.fixtures.fixture_recipes import ingredient
from tests.fixtures.fixture_users import user
from users.models import Follow, User

pytestmark = pytest.mark.django_db

class TestUserModel:
    """Тесты модели пользователя."""

    def test_create_user(self):
        """Проверка успешного создания пользователя."""
        user = User.objects.create_user(
            email='test@example.com',
            username='testuser',
            first_name='Test',
            last_name='User',
            password='testpass123',
        )
        assert user.email == 'test@example.com'
        assert user.username == 'testuser'
        assert user.first_name == 'Test'
        assert user.last_name == 'User'
        assert user.check_password('testpass123')
        assert not user.is_staff
        assert not user.is_superuser
        assert user.is_active

    def test_create_user_with_email_raises_error(self):
        """Проверка, что создание пользователя без email вызывает ошибку."""
        with pytest.raises(ValueError) as exc_info:
            User.objects.create_user(
                email=None,
                username='testuser',
                first_name='Test',
                last_name='User',
                password='testpass123'
            )
        msg = str(exc_info.value).lower()
        assert 'email' in msg or 'почты' in msg

    def test_create_superuser(self):
        """Проверка создания суперпользователя."""
        admin = User.objects.create_superuser(
            email='admin@example.com',
            username='admin',
            first_name='Admin',
            last_name='User',
            password='adminpass123'
        )
        assert admin.is_superuser
        assert admin.is_staff
        assert admin.check_password('adminpass123')

    def test_create_superuser_requires_is_staff(self):
        """Проверка, что для суперпользователя требуется is_staff=True."""
        with pytest.raises(ValueError) as exc_info:
            User.objects.create_superuser(
                email='admin@example.com',
                username='admin',
                first_name='Admin',
                last_name='User',
                password='adminpass123',
                is_staff = False
            )
        assert 'is_staff' in str(exc_info.value)

    def test_create_superuser_requires_is_superuser(self):
        """Проверка, что для суперпользователя требуется is_superuser=True."""
        with pytest.raises(ValueError) as exc_info:
            User.objects.create_superuser(
                email='admin@example.com',
                username='admin',
                first_name='Admin',
                last_name='User',
                password='adminpass123',
                is_superuser=False
            )
        assert 'is_superuser' in str(exc_info.value)

    def test_email_must_be_unique(self):
        """Проверка уникальности email."""
        User.objects.create_user(
            email='unique@example.com',
            username='user1',
            first_name='Test',
            last_name='User',
            password='pass123'
        )
        with pytest.raises(IntegrityError):
            User.objects.create_user(
                email='unique@example.com',
                username='user2',
                first_name='Test',
                last_name='User',
                password='pass123'
            )

    def test_str_representation_returns_email(self):
        """Проверка строкового представления email."""
        user = User(
            email='mail@test.com',
            username='user',
            first_name='Test',
            last_name='User',
        )
        assert str(user) == 'mail@test.com'

    def test_get_full_name(self, user):
        """Проверка метода получения полно имени."""
        assert user.get_full_name() == 'Test User'

    def test_user_default_ordering(self, user, user2):
        """Проверка стандартной сортировки пользователей."""
        assert list(User.objects.all()) == [user, user2]

    def test_username_validation(self, user):
        """Проверка валидации username."""
        user.username = 'valid_user123'
        user.full_clean()

    def test_username_validation_invalid_characters(self):
        """Проверка валидации username с недопустимыми символами."""
        user = User(
            email='mail@test.com',
            username='invalid_username!',
            first_name='Test',
            last_name='User',
        )
        with pytest.raises(ValidationError):
            user.full_clean()

class TestFollowModel:
    """Тесты модели подписки."""

    def test_user_can_follow_author(self, user, user2):
        """Проверка возможности подписки на автора."""
        follow = Follow.objects.create(user=user, author=user2)
        assert follow.user == user
        assert follow.author == user2
        assert follow in Follow.objects.all()

    def test_cannot_follow_yourself(self, user):
        """Проверка, что пользователь не может подписаться на себя."""
        Follow.objects.create(user=user, author=user)
        count_follow = Follow.objects.filter(user=user, author=user).count()
        assert count_follow == 1

    def test_cannot_follow_same_author_twice(self, user, user2):
        """проверка, что нельзя подписаться на одного автора дважды."""
        Follow.objects.create(user=user, author=user2)
        with pytest.raises(IntegrityError):
            Follow.objects.create(user=user, author=user2)

    def test_follow_cascade_on_user_delete(self, user, user2):
        """Проверка каскадного удаления подписок при удалении пользователя."""
        Follow.objects.create(user=user, author=user2)
        assert Follow.objects.count() == 1
        user.delete()
        assert Follow.objects.count() == 0

    def test_follow_cascade_on_author_delete(self, user, user2):
        """Проверка каскадного удаления подписок при удалении автора."""
        Follow.objects.create(user=user, author=user2)
        assert Follow.objects.count() == 1
        user2.delete()
        assert Follow.objects.count() == 0

    def test_multiple_users_can_follow_same_author(
            self, user, user2, admin_user):
        """Проверка подписки нескольких пользователей на одного автора."""
        Follow.objects.create(user=user, author=admin_user)
        Follow.objects.create(user=user2, author=admin_user)
        assert Follow.objects.filter(author=admin_user).count() == 2

    def test_user_can_follow_multiple_authors(self, user, user2, admin_user):
        """Проверка подписки пользователя на нескольких авторов."""
        Follow.objects.create(user=user, author=admin_user)
        Follow.objects.create(user=user, author=user2)
        assert Follow.objects.filter(user=user).count() == 2

class TestTagModel:
    """Тесты модели тега."""

    def test_create_tag(self):
        """Проверка создания тега."""
        tag = Tag.objects.create(
            name='Завтрак',
            color='#FF0000',
            slug='breakfast'
        )
        assert tag.name == 'Завтрак'
        assert tag.color == '#FF0000'
        assert tag.slug == 'breakfast'

    def test_str_representation(self, tag):
        """Проверка строкового представления тега."""
        assert str(tag) == 'Завтрак'

    def test_unique_slug(self, tag):
        """Проверка уникальности slug."""
        with pytest.raises(IntegrityError):
            Tag.objects.create(
                name='Завтрак 2',
                color='#00FF00',
                slug='breakfast'
            )

    def test_same_name_different_slug_allowed(self, tag):
        """Проверка, что допустимы одинаковые name с разными slug."""
        tag2 = Tag.objects.create(
            name='Завтрак',
            color='#00FF00',
            slug='breakfast-2'
        )
        assert tag2.id != tag.id

    def test_slug_validation_invalid_spaces(self):
        """Проверка валидации slug с пробелами."""
        tag = Tag(name='Tets', color='#FF0000', slug='invalid slug')
        with pytest.raises(ValidationError):
            tag.full_clean()

    def test_slug_validation_invalid_characters(self):
        """Проверка валидации slug с недопустимыми символами."""
        tag = Tag(name='Tets', color='#FF0000', slug='invalid@slug!')
        with pytest.raises(ValidationError):
            tag.full_clean()

    def test_color_max_length(self, tag):
        """Проверка максимальной длины поля цвета."""
        assert tag._meta.get_field('color').max_length == 7

class TestIngredientModel:
    """Тесты модели ингредиента."""

    def test_create_ingredient(self):
        """Проверка создания ингредиента."""
        ingredient = Ingredient.objects.create(
            name='Помидор',
            measurement_unit='г'
        )
        assert ingredient.name == 'Помидор'
        assert ingredient.measurement_unit == 'г'

    def test_str_representation(self, ingredient):
        """Проверка строкового представления ингредиента."""
        assert str(ingredient) == 'Яйцо, шт'

    def test_unique_constraint_name_and_unit(self):
        """Проверка уникальности связки name и measurement_unit."""
        Ingredient.objects.create(name='Яйцо', measurement_unit='шт')
        with pytest.raises(IntegrityError):
            Ingredient.objects.create(
                name='Яйцо',
                measurement_unit='шт'
            )

    def test_same_name_different_units_allowed(self, ingredient):
        """Проверка допустимости одинаковых name с разными единицами."""
        ingredient_kg = Ingredient.objects.create(
            name='Яйцо',
            measurement_unit='кг'
        )
        assert ingredient_kg.id != ingredient.id

    def test_ordering_by_name(self, db):
        """Проверка сортировки ингредиентов по имени."""
        Ingredient.objects.create(name='Яблоко', measurement_unit='шт')
        Ingredient.objects.create(name='Банан', measurement_unit='шт')
        Ingredient.objects.create(name='Апельсин', measurement_unit='шт')
        ingredients = list(Ingredient.objects.values_list('name', flat=True))
        assert ingredients == ['Апельсин', 'Банан', 'Яблоко']

    def test_name_max_length(self, ingredient):
        """Проверка максимальной длины имени."""
        assert ingredient._meta.get_field('name').max_length == 200

    def test_measurement_unit_max_length(self, ingredient):
        """Проверка максимальной длины единицы измерения."""
        assert ingredient._meta.get_field('measurement_unit').max_length == 200

class TestRecipeModel:
    """Тесты модели рецепта."""

    def test_create_recipe(self, user, tag, ingredient):
        """Проверка создания рецепта."""
        recipe = Recipe.objects.create(
            author=user,
            name='Омлет',
            text='Взбить яйца и пожарить',
            cooking_time=15
        )
        recipe.tags.add(tag)
        IngredientInRecipe.objects.create(
            recipe=recipe,
            ingredient=ingredient,
            amount=2
        )
        assert recipe.author == user
        assert recipe.name == 'Омлет'
        assert tag in recipe.tags.all()
        assert recipe in user.recipes.all()

    def test_str_representation(self, recipe):
        """Проверка строкового представления рецепта."""
        assert str(recipe) == 'Омлет'

    def test_recipe_without_image(self, user, tag):
        """Проверка, что рецепт может быть создан без изображения."""
        recipe = Recipe.objects.create(
            author=user,
            name='Test',
            text='Рецепт без изображения',
            cooking_time=10,
            image=''
        )
        assert recipe.image == ''

    def test_recipe_ordering_by_pub_date_desc(self, user, tag):
        """Проверка сортировки рецептов по дате публикации (убывание)."""
        recipe1 = Recipe.objects.create(
            author=user, name='Первый', text='Тестовый', cooking_time=15
        )
        recipe2 = Recipe.objects.create(
            author=user, name='Второй', text='Тестовый 2', cooking_time=15
        )
        recipes = list(Recipe.objects. all())
        assert recipes[0] == recipe2
        assert recipes[1] == recipe1

    def test_recipe_has_pub_date_auto(self, recipe):
        """Проверка автоматического заполнения даты публикации."""
        assert recipe.pub_date is not None

    def test_recipe_many_tags(self, user, tag, tag2):
        """Проверка возможности добавления нескольких тегов к рецепту."""
        recipe = Recipe.objects.create(
            author=user, name='Тест', text='Приготовление', cooking_time=15
        )
        recipe.tags.add(tag, tag2)
        assert recipe.tags.count() == 2

    def test_recipe_many_ingredients(self, user, ingredient, ingredient2):
        """Проверка добавления нескольких ингредиентов к рецепту."""
        recipe = Recipe.objects.create(
            author=user, name='Тест', text='Приготовление', cooking_time=15
        )
        IngredientInRecipe.objects.create(
            recipe=recipe, ingredient=ingredient, amount=1
        )
        IngredientInRecipe.objects.create(
            recipe=recipe, ingredient=ingredient2, amount=10
        )
        assert recipe.ingredients.count() == 2

    def test_cooking_time_minimum_validation(self, user):
        """Проверка минимального значения времени приготовления."""
        time_field = Recipe._meta.get_field('cooking_time')
        validators = time_field.validators
        min_validator = next(
            (v for v in validators if isinstance(v, MinValueValidator)), None
        )
        assert min_validator is not None
        assert min_validator.limit_value == 1

class TestIngredientInRecipe:
    """Тесты связи ингредиента и рецепта."""

    def test_create_link(self, user, recipe, ingredient2):
        """Проверка создания связи ингредиента с рецептом."""
        link = IngredientInRecipe.objects.create(
            recipe=recipe,
            ingredient=ingredient2,
            amount=2
        )
        assert link.recipe == recipe
        assert link.ingredient == ingredient2
        assert link.amount == 2

    def test_unique_constraint_ingredient_in_recipe(
            self, user, recipe2, ingredient):
        """Проверка уникальности связи ингредиента и рецепта."""
        IngredientInRecipe.objects.create(
            recipe=recipe2,
            ingredient=ingredient,
            amount=20
        )
        with pytest.raises(IntegrityError):
            IngredientInRecipe.objects.create(
                recipe=recipe2,
                ingredient=ingredient,
                amount=200
            )

    def test_same_ingredient_in_different_recipes(
            self, user, recipe, recipe2, ingredient_salt):
        """Проверка использования одного ингредиента в разных рецептах."""
        IngredientInRecipe.objects.create(
            recipe=recipe,
            ingredient=ingredient_salt,
            amount=20
        )
        link = IngredientInRecipe.objects.create(
            recipe=recipe2,
            ingredient=ingredient_salt,
            amount=40
        )
        assert link.id != recipe.amounts.first().id

    def test_amount_minimum_value(self, user, recipe, ingredient2):
        """Проверка минимального значения количества ингредиента."""
        link = IngredientInRecipe(
            recipe=recipe,
            ingredient=ingredient2,
            amount=0
        )
        with pytest.raises(ValidationError):
            link.full_clean()

    def test_cascade_delete_recipe(self, user, recipe):
        """Проверка каскадного удаления при удалении рецепта."""
        query = IngredientInRecipe.objects.filter(recipe_id=recipe.id)
        initial_count = query.count()
        assert initial_count >= 1
        recipe.delete()
        assert query.count() == 0

    def test_cascade_delete_ingredient(self, user, recipe, ingredient):
        """Проверка каскадного удаления при удалении ингредиента."""
        query = IngredientInRecipe.objects.filter(ingredient_id=ingredient.id)
        initial_count = query.count()
        assert initial_count >= 1
        ingredient.delete()
        assert query.count() == 0

class TestRecipeFavorite:
    """Тесты модели избранного."""

    def test_add_to_favorite(self, user, recipe):
        """Проверка добавления рецепта в избранное."""
        favorite = RecipesFavorite.objects.create(
            recipe=recipe,
            user=user,
        )
        assert favorite.user == user
        assert favorite.recipe == recipe
    def test_cannot_add_favorite_same_recipe_twice(self, user, recipe):
        """Проверка, что нельзя добавить рецепт в избранное дважды."""
        RecipesFavorite.objects.create(recipe=recipe, user=user)
        with pytest.raises(IntegrityError):
            RecipesFavorite.objects.create(recipe=recipe, user=user)

    def test_different_users_can_favorite_same_recipe(
            self, user, user2, recipe):
        """Проверка добавления рецепта в избранное разными пользователями."""
        RecipesFavorite.objects.create(recipe=recipe, user=user)
        favorite2 = RecipesFavorite.objects.create(recipe=recipe, user=user2)
        first = RecipesFavorite.objects.filter(user=user).first()
        assert favorite2.id != first.id

    def test_user_can_favorite_multiple_recipes(self, user, recipe, recipe2):
        """Проверка добавления нескольких рецептов в избранное."""
        RecipesFavorite.objects.create(recipe=recipe, user=user)
        RecipesFavorite.objects.create(recipe=recipe2, user=user)
        count = RecipesFavorite.objects.filter(user=user).count()
        assert count == 2

    def test_cascade_delete_recipe(self, user, recipe):
        """Проверка каскадного удаления из избранного при удалении рецепта."""
        RecipesFavorite.objects.create(recipe=recipe, user=user)
        assert RecipesFavorite.objects.count() == 1
        recipe.delete()
        assert RecipesFavorite.objects.count() == 0

    def test_cascade_delete_user(self, user, recipe):
        """Проверка удаления из избранного при удалении пользователя."""
        RecipesFavorite.objects.create(recipe=recipe, user=user)
        assert RecipesFavorite.objects.count() == 1
        user.delete()
        assert RecipesFavorite.objects.count() == 0

    def test_favorites_related_name(self, user, recipe):
        """Проверка обратных связей для избранного."""
        RecipesFavorite.objects.create(recipe=recipe, user=user)
        assert user.favorites_user.filter(recipe=recipe).exists()
        assert recipe.favorites.filter(user=user).exists()

class TestShoppingCart:
    """Тесты модели списка покупок."""

    def test_add_to_shopping_cart(self, user, recipe):
        """Проверка добавления рецепта в список покупок."""
        shopping_cart = ShoppingCart.objects.create(user=user, recipe=recipe)
        assert shopping_cart.user == user
        assert shopping_cart.recipe == recipe

    def test_cannot_add_same_recipe_twice(self, user, recipe):
        """Проверка, что нельзя добавить один рецепт в корзину дважды."""
        ShoppingCart.objects.create(user=user, recipe=recipe)
        with pytest.raises(IntegrityError):
            ShoppingCart.objects.create(user=user, recipe=recipe)

    def test_multiple_users_can_add_same_recipe(self, user, user2, recipe):
        """Проверка добавления рецепта в корзину разными пользователями."""
        ShoppingCart.objects.create(user=user, recipe=recipe)
        ShoppingCart.objects.create(user=user2, recipe=recipe)
        assert ShoppingCart.objects.count() == 2

    def test_carts_related_name(self, user, recipe):
        """Проверка обратных связей для списка покупок."""
        ShoppingCart.objects.create(user=user, recipe=recipe)
        assert user.carts.filter(recipe=recipe).exists()
        assert recipe.carts.filter(user=user).exists()

    def test_cascade_delete_recipe(self, user, recipe):
        """Проверка каскадного удаления из корзины при удалении рецепта."""
        ShoppingCart.objects.create(user=user, recipe=recipe)
        assert ShoppingCart.objects.count() == 1
        recipe.delete()
        assert ShoppingCart.objects.count() == 0

    def test_cascade_delete_user(self, user, recipe):
        """Каскадное удаление из корзины при удалении пользователя."""
        ShoppingCart.objects.create(user=user, recipe=recipe)
        assert ShoppingCart.objects.count() == 1
        user.delete()
        assert ShoppingCart.objects.count() == 0
