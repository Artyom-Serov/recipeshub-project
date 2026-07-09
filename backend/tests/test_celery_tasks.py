from unittest.mock import patch, MagicMock

from django.test import TestCase

from recipes.tasks import generate_shopping_cart_csv, save_recipe_image


class TestGenerateShoppingCartCSV(TestCase):
    """Тесты для задачи генерации CSV."""

    def setUp(self):
        from recipes.models import (
            Ingredient, IngredientInRecipe, Recipe,
            ShoppingCart, Tag, User
        )
        self.user = User.objects.create_user(
            email='test@example.com',
            username='testuser',
            first_name='Test',
            last_name='User',
            password='testpass123'
        )
        self.tag = Tag.objects.create(
            name='Завтрак', color='#FF0000', slug='breakfast'
        )
        self.ingredient = Ingredient.objects.create(
            name='Молоко', measurement_unit='мл'
        )
        self.recipe = Recipe.objects.create(
            author=self.user,
            name='Блинчики',
            text='Рецепт',
            cooking_time=15
        )
        self.recipe.tags.add(self.tag)
        IngredientInRecipe.objects.create(
            recipe=self.recipe,
            ingredient=self.ingredient,
            amount=250
        )
        ShoppingCart.objects.create(user=self.user, recipe=self.recipe)

    @patch('recipes.tasks.os.makedirs')
    @patch('recipes.tasks.open', create=True)
    def test_csv_generation_creates_file(self, mock_open, mock_makedirs):
        mock_open.return_value.__enter__ = lambda s: s
        mock_open.return_value.__exit__ = MagicMock(return_value=False)

        result = generate_shopping_cart_csv(self.user.id)

        self.assertEqual(result, f'shopping_carts/{self.user.id}.csv')

    def test_csv_generation_with_no_cart(self):
        from recipes.models import ShoppingCart
        ShoppingCart.objects.all().delete()

        result = generate_shopping_cart_csv(self.user.id)

        self.assertEqual(result, f'shopping_carts/{self.user.id}.csv')


class TestSaveRecipeImage(TestCase):
    """Тесты для задачи сохранения изображения."""

    def setUp(self):
        from recipes.models import Recipe, User
        self.user = User.objects.create_user(
            email='test@example.com',
            username='testuser',
            first_name='Test',
            last_name='User',
            password='testpass123'
        )
        self.recipe: Recipe = Recipe.objects.create(
            author=self.user,
            name='Блинчики',
            text='Рецепт',
            cooking_time=15
        )

    def test_image_save_updates_recipe(self):
        # Минимальное корректное base64-изображение (белый пиксель 1x1 PNG)
        import base64
        minimal_png = (
            b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01'
            b'\x00\x00\x00\x01\x08\x02\x00\x00\x00\x90wS\xde\x00'
            b'\x00\x00\x0cIDATx\x9cc\xf8\x0f\x00\x00\x01\x01\x00'
            b'\x05\x18\xd8N\x00\x00\x00\x00IEND\xaeB`\x82'
        )
        image_b64 = base64.b64encode(minimal_png).decode()

        with patch('recipes.tasks.os.makedirs'):
            with patch('builtins.open', MagicMock()):
                result = save_recipe_image(
                    self.recipe.id, image_b64, 'image/png'
                )

        self.assertIsNotNone(result)

    def test_image_save_handles_missing_recipe(self):
        result = save_recipe_image(99999, 'dGVzdA==', 'image/png')
        self.assertIsNone(result)
