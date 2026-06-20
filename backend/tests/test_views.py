"""Тесты представлений приложений recipes и users."""

import pytest
from rest_framework import status

from recipes.models import RecipesFavorite, ShoppingCart

pytestmark = pytest.mark.django_db


class TestTagsViewSet:
    """Тесты представлений тегов."""

    def test_tag_list_view(self, api_client):
        """Тесты получения списка тегов."""
        response = api_client.get('/api/tags/')
        assert response.status_code == status.HTTP_200_OK

    def test_tags_retrieve_view(self, api_client, tag):
        """Тесты получения конкретного тега."""
        response = api_client.get(f'/api/tags/{tag.id}/')
        assert response.status_code == status.HTTP_200_OK
        assert response.data['name'] == tag.name


class TestIngredientsViewSet:
    """Тесты представлений ингредиентов."""

    def test_ingredients_list_view(self, api_client):
        """Тест получения списка ингредиентов."""
        response = api_client.get('/api/ingredients/')
        assert response.status_code == status.HTTP_200_OK

    def test_ingredients_retrieve_view(self, api_client, ingredient):
        """Тест получения конкретного ингредиента."""
        response = api_client.get(f'/api/ingredients/{ingredient.id}/')
        assert response.status_code == status.HTTP_200_OK
        assert response.data['name'] == ingredient.name


class TestRecipesViewSet:
    """Тесты представлений рецептов."""

    def test_recipe_list_view(self, api_client):
        """Тест получения списка рецептов."""
        response = api_client.get('/api/recipes/')
        assert response.status_code == status.HTTP_200_OK

    def test_recipe_retrieve_view(self, api_client, recipe):
        """тест получения конкретного рецепта."""
        response = api_client.get(f'/api/recipes/{recipe.id}/')
        assert response.status_code == status.HTTP_200_OK
        assert response.data['name'] == recipe.name

    def test_recipe_create_view(
            self, authenticated_client, tag, ingredient, test_image_base64):
        """Тест создания рецепта."""
        data = {
            'ingredients': [{'id': ingredient.id, 'amount': 2}],
            'tags': [tag.id],
            'name': 'Тестовый рецепт',
            'text': 'Описание тестового рецепта',
            'cooking_time': 60,
            'image': f'data:image/png;base64,{test_image_base64}',
        }
        response = authenticated_client.post(
            '/api/recipes/', data, format='json'
        )
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['name'] == 'Тестовый рецепт'

    def test_recipe_update_view(
            self, authenticated_client, recipe, tag2, test_image_base64):
        """Тест обновления рецепта."""
        ingr_id = recipe.ingredients.first().id
        data = {
            'ingredients': [{'id': ingr_id, 'amount': 2}],
            'tags': [tag2.id],
            'name': 'Обновленный рецепт',
            'text': 'Новое описание',
            'cooking_time': 30,
            'image': f'data:image/png;base64,{test_image_base64}',
        }
        response = authenticated_client.put(
            f'/api/recipes/{recipe.id}/', data, format='json'
        )
        assert response.status_code == status.HTTP_200_OK
        assert response.data['name'] == 'Обновленный рецепт'

    def test_recipe_delete_view(self, authenticated_client, recipe):
        """Тест удаления рецепта."""
        response = authenticated_client.delete(f'/api/recipes/{recipe.id}/')
        assert response.status_code == status.HTTP_204_NO_CONTENT


class TestCustomUserViewSet:
    """Тесты представлений пользователей."""

    def test_user_list_view(self, api_client):
        """Тест получения списка пользователей."""
        response = api_client.get('/api/users/')
        assert response.status_code == status.HTTP_200_OK

    def test_user_retrieve_view(self, api_client, user):
        """Тест получения конкретного пользователя."""
        response = api_client.get(f'/api/users/{user.id}/')
        assert response.status_code == status.HTTP_200_OK
        assert response.data['email'] == user.email

    def test_user_me_view(self, authenticated_client, user):
        """Тест получения текущего пользователя."""
        response = authenticated_client.get('/api/users/me/')
        assert response.status_code == status.HTTP_200_OK
        assert response.data['email'] == user.email

    def test_user_subscribe_view(self, authenticated_client, user2):
        """Тест подписки на пользователя."""
        url = f'/api/users/{user2.id}/subscribe/'
        response = authenticated_client.post(url)
        assert response.status_code == status.HTTP_201_CREATED

    def test_user_unsubscribe_view(self, authenticated_client, user2, follow):
        """Тест отписки от пользователя."""
        response = authenticated_client.delete(
            f'/api/users/{user2.id}/subscribe/'
        )
        assert response.status_code == status.HTTP_204_NO_CONTENT


class TestRecipeViewSetActions:
    """Тесты действий RecipeViewSet."""
    def test_favorite_action(self, authenticated_client, recipe):
        """Тест добавления в избранное."""
        response = authenticated_client.post(
            f'/api/recipes/{recipe.id}/favorite/'
        )
        assert response.status_code == status.HTTP_201_CREATED

    def test_delete_favorite_action(self, authenticated_client, user, recipe):
        """Тест удаления из избранного."""
        RecipesFavorite.objects.create(user=user, recipe=recipe)
        response = authenticated_client.delete(
            f'/api/recipes/{recipe.id}/favorite/'
        )
        assert response.status_code == status.HTTP_204_NO_CONTENT

    def test_shopping_cart_action(self, authenticated_client, recipe):
        """Тест добавления в корзину."""
        response = authenticated_client.post(
            f'/api/recipes/{recipe.id}/shopping_cart/'
        )
        assert response.status_code == status.HTTP_201_CREATED

    def test_delete_shopping_cart_action(
        self, authenticated_client, user, recipe
    ):
        """Тест удаления из корзины."""
        ShoppingCart.objects.create(user=user, recipe=recipe)
        response = authenticated_client.delete(
            f'/api/recipes/{recipe.id}/shopping_cart/'
        )
        assert response.status_code == status.HTTP_204_NO_CONTENT

    def test_download_shopping_cart_action(
        self, authenticated_client, user, recipe
    ):
        """Тест загрузки списка покупок."""
        ShoppingCart.objects.create(user=user, recipe=recipe)
        response = authenticated_client.get(
            '/api/recipes/download_shopping_cart/'
        )
        assert response.status_code == status.HTTP_200_OK
        assert response['Content-Type'] == 'text/csv'
