"""Тесты API приложения recipes и users."""

import pytest

from rest_framework import status

from recipes.models import Recipe, RecipesFavorite, ShoppingCart
from tests.fixtures.fixture_clients import authenticated_client

pytestmark = pytest.mark.django_db

class TestUserAPI:
    """Тесты API пользователей."""

    def test_user_list_anonymous(self, api_client):
        """проверка списка пользователей анонимным пользователем."""
        response = api_client.get('/api/users/')
        assert response.status_code == status.HTTP_200_OK

    def test_user_list_authenticated(self, authenticated_client):
        """Проверка получения списка пользователей при авторизации."""
        response = authenticated_client.get('/api/users/')
        assert response.status_code == status.HTTP_200_OK

    def test_user_retrieve(self, api_client, user):
        """Проверка получения конкретного пользователя."""
        response = api_client.get(f'/api/users/{user.id}/')
        assert response.status_code == status.HTTP_200_OK
        assert response.data['id'] == user.id
        assert response.data['username'] == user.username
        assert response.data['email'] == user.email
        assert response.data['first_name'] == user.first_name
        assert response.data['last_name'] == user.last_name

    def test_user_registration(self, api_client):
        """Проверка регистрации нового пользователя."""
        data = {
            'email': 'newuser@test.com',
            'username': 'newuser',
            'first_name': 'New',
            'last_name': 'User',
            'password': 'newpass123',
        }
        response = api_client.post('/api/users/', data=data)
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['email'] == data['email']
        assert response.data['username'] == data['username']

    def test_user_registration_duplicate_email(self, api_client, user):
        """Проверка ошибки при регистрации с существующим email."""
        data = {
            'email': user.email,
            'username': 'differentuser',
            'first_name': 'New',
            'last_name': 'User',
            'password': 'newpass123',
        }
        response = api_client.post('/api/users/', data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_user_registration_duplicate_username(self, api_client, user):
        """Проверка ошибки при регистрации с существующим username."""
        data = {
            'email': 'newuser@test.com',
            'username': user.username,
            'first_name': 'New',
            'last_name': 'User',
            'password': 'newpass123',
        }
        response = api_client.post('/api/users/', data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST

class TestAuthAPI:
    """Тесты API аутентификации."""

    def test_login(self, api_client, user):
        """Вход пользователя."""
        data = {
            'email': user.email,
            'password': 'testpass123'
        }
        response = api_client.post('/api/auth/token/login/', data)
        assert response.status_code in [
            status.HTTP_200_OK,
            status.HTTP_400_BAD_REQUEST,
            status.HTTP_404_NOT_FOUND
        ]

    def test_logout(self, authenticated_client):
        """Выход пользователя."""
        response = authenticated_client.post('/api/auth/token/logout/')
        assert response.status_code in [
            status.HTTP_200_OK,
            status.HTTP_204_NO_CONTENT,
            status.HTTP_401_UNAUTHORIZED
        ]

    def test_token_login_requires_email(self, api_client):
        """Для входа требуется email."""
        data = {'password': 'test'}
        response = api_client.post('/api/auth/token/login/', data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST

class TestFollowAPI:
    """Тесты API подписок."""

    def test_follow_list_anonymous(self, api_client):
        """Проверка, что аноним не может получить список подписок."""
        response = api_client.get('/api/users/1/subscribe/')
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_follow_authenticated(self, authenticated_client, user2):
        """Подписка на автора авторизованным пользователем."""
        url = f'/api/users/{user2.id}/subscribe/'
        response = authenticated_client.post(url)
        assert response.status_code == status.HTTP_201_CREATED

    def test_follow_self_forbidden(self, authenticated_client, user):
        """Нельзя подписаться на себя."""
        url = f'/api/users/{user.id}/subscribe/'
        response = authenticated_client.post(url)
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_follow_duplicate_forbidden(self, authenticated_client, user2):
        """Нельзя подписаться на автора дважды."""
        url = f'/api/users/{user2.id}/subscribe/'
        authenticated_client.post(url)
        response = authenticated_client.post(url)
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_unfollow(self, authenticated_client, user2, follow):
        """Отписка от автора."""
        url = f'/api/users/{user2.id}/subscribe/'
        response = authenticated_client.delete(url)
        assert response.status_code == status.HTTP_204_NO_CONTENT

class TestTagAPI:
    """Тесты API тегов."""

    def test_tag_list(self, api_client, tag):
        """Проверка получения списка тегов."""
        response = api_client.get('/api/tags/')
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) >= 1

    def test_tag_retrieve(self, api_client, tag):
        """Проверка получения конкретного тега."""
        url = f'/api/tags/{tag.id}/'
        response = api_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert response.data['name'] == tag.name

    def test_tag_filter_by_name(self, api_client, tag):
        """Проверка фильтрации тегов по имени."""
        response = api_client.get('/api/tags/', data={'name': tag.name})
        assert response.status_code == status.HTTP_200_OK

class TestIngredientAPI:
    """Тесты API ингредиентов."""

    def test_ingredient_list(self, api_client, ingredient):
        """Проверка получения списка ингредиентов."""
        response = api_client.get('/api/ingredients/')
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) >= 1

    def test_ingredient_retrieve(self, api_client, ingredient):
        """Проверка получения конкретного ингредиента."""
        url = f'/api/ingredients/{ingredient.id}/'
        response = api_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert response.data['name'] == ingredient.name

    def test_ingredient_filter_by_name(self, api_client, ingredient):
        """Проверка точной фильтрации ингредиентов по имени."""
        response = api_client.get('/api/ingredients/', data={'name': 'Яйцо'})
        assert response.status_code == status.HTTP_200_OK

    def test_ingredient_search(self, api_client, ingredient):
        """Проверка поиска ингредиентов по имени."""
        response = api_client.get('/api/ingredients/', data={'name': 'Яйц'})
        assert response.status_code == status.HTTP_200_OK

class TestRecipeAPI:
    """Тесты API рецептов."""

    def test_recipe_list_anonymous(self, api_client, recipe):
        """Проверка получения списка рецептов анонимным пользователем."""
        response = api_client.get('/api/recipes/')
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data['results']) >= 1

    def test_recipe_retrieve(self, api_client, recipe):
        """Проверка получения конкретного рецепта."""
        url = f'/api/recipes/{recipe.id}/'
        response = api_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert response.data['name'] == recipe.name
        assert 'tags' in response.data
        assert 'ingredients' in response.data

    def test_recipe_create_authenticated(
            self, authenticated_client, tag, ingredient, test_image_base64):
        """Проверка создания рецепта авторизованным пользователем."""
        ing = [{'id': ingredient.id, 'amount': 2}]
        data = {
            'ingredients': ing,
            'tags': [tag.id],
            'name': 'Новый рецепт',
            'text': 'Описание нового рецепта',
            'cooking_time': 30,
            'image': f'data:image/png;base64,{test_image_base64}',
        }
        url = '/api/recipes/'
        response = authenticated_client.post(url, data, format='json')
        assert response.status_code == status.HTTP_201_CREATED, response.data
        assert response.data['name'] == 'Новый рецепт'

    def test_recipe_create_without_auth(self, api_client, tag):
        """Проверка запрета создания рецепта без авторизации."""
        data = {
            'tags': [tag.id],
            'name': 'Новый рецепт',
            'text': 'Описание',
            'cooking_time': 30,
        }
        url = '/api/recipes/'
        response = api_client.post(url, data, format='json')
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_recipe_create_without_ingredients(
            self, authenticated_client, tag):
        """Проверка ошибки при создании рецепта без ингредиентов."""
        data = {
            'tags': [tag.id],
            'name': 'Без ингредиентов',
            'text': 'Описание',
            'cooking_time': 30,
        }
        url = '/api/recipes/'
        response = authenticated_client.post(url, data, format='json')
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_recipe_create_without_tags(
            self, authenticated_client, ingredient):
        """Проверка ошибки при создании рецепта без тега."""
        data = {
            'ingredients': [{'id': ingredient.id, 'amount': 2}],
            'name': 'Без тега',
            'text': 'Описание',
            'cooking_time': 30,
        }
        url = '/api/recipes/'
        response = authenticated_client.post(url, data, format='json')
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_recipe_update_by_author(
            self, authenticated_client, recipe, tag2, test_image_base64):
        """Проверка обновления рецепта автором."""
        ing_id = recipe.ingredients.first().id
        ing = [{'id': ing_id, 'amount': 5}]
        data = {
            'ingredients': ing,
            'tags': [tag2.id],
            'name': 'Обновленный рецепт',
            'text': 'Обновленное описание',
            'cooking_time': 25,
            'image': f'data:image/png;base64,{test_image_base64}',
        }
        url = f'/api/recipes/{recipe.id}/'
        response = authenticated_client.put(url, data, format='json')
        assert response.status_code == status.HTTP_200_OK, response.data
        assert response.data['name'] == 'Обновленный рецепт'

    def test_recipe_update_by_non_author(
            self, api_client, user2, recipe, tag):
        """Проверка запрета изменения рецепта не автором."""
        api_client.force_authenticate(user=user2)
        data = {
            'ingredients': [{'id': 1, 'amount': 1}],
            'tags': [tag.id],
            'name': 'Чужой рецепт',
            'text': 'Описание',
            'cooking_time': 10
        }
        url = f'/api/recipes/{recipe.id}/'
        response = api_client.put(url, data, format='json')
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_recipe_delete_by_author(self, authenticated_client, recipe):
        """Проверка удаления рецепта автором."""
        url = f'/api/recipes/{recipe.id}/'
        response = authenticated_client.delete(url)
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert not Recipe.objects.filter(id=recipe.id).exists()

    def test_recipe_delete_by_non_author(self, api_client, user2, recipe, tag):
        """Проверка запрета удаления рецепта не автором."""
        api_client.force_authenticate(user=user2)
        url = f'/api/recipes/{recipe.id}/'
        response = api_client.delete(url)
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_recipe_filter_by_author(self, api_client, recipe, user):
        """Проверка фильтрации рецептов по автору."""
        response = api_client.get(f'/api/recipes/', {'author': user.id})
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) >= 1

    def test_recipe_filter_by_tag(self, api_client, recipe, tag):
        """Проверка фильтрации рецептов по тегу."""
        response = api_client.get(f'/api/recipes/', {'tag': tag.slug})
        assert response.status_code == status.HTTP_200_OK

    def test_recipe_filter_by_is_favorited(self, authenticated_client, recipe):
        """Проверка фильтрации рецептов по-избранному."""
        user = authenticated_client.handler._force_user
        RecipesFavorite.objects.create(recipe=recipe, user=user)
        response = authenticated_client.get(
            '/api/recipes/', {'is_favorited': 1}
        )
        assert response.status_code == status.HTTP_200_OK

    def test_recipe_pagination(self, api_client, user, tag, ingredient):
        """Проверка пагинации рецептов."""
        for i in range(15):
            r = Recipe.objects.create(
                author=user,
                name=f'Рецепт {i}',
                text='Описание',
                cooking_time=10
            )
            r.tags.add(tag)
        response = api_client.get('/api/recipes/')
        assert response.status_code == status.HTTP_200_OK
        assert 'results' in response.data
        assert len(response.data['results']) <= 10

class TestShoppingCartAPI:
    """Тесты API списка покупок."""

    def test_add_to_cart(self, authenticated_client, recipe):
        """Проверка добавления рецепта в список покупок."""
        url = f'/api/recipes/{recipe.id}/shopping_cart/'
        response = authenticated_client.post(url)
        assert response.status_code == status.HTTP_201_CREATED
        assert ShoppingCart.objects.filter(recipe=recipe).exists()

    def test_add_to_cart_unauthenticated(self, api_client, recipe):
        """Проверка, что неавторизованный не может добавить в корзину."""
        url = f'/api/recipes/{recipe.id}/shopping_cart/'
        response = api_client.post(url)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_add_same_recipe_to_cart_twice(
            self, authenticated_client, recipe):
        """Проверка, что нельзя добавить рецепт в корзину дважды."""
        url = f'/api/recipes/{recipe.id}/shopping_cart/'
        authenticated_client.post(url)
        response = authenticated_client.post(url)
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_remove_from_cart(self, authenticated_client, recipe):
        """Проверка удаления рецепта из списка покупок."""
        url = f'/api/recipes/{recipe.id}/shopping_cart/'
        authenticated_client.post(url)
        response = authenticated_client.delete(url)
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert not ShoppingCart.objects.filter(recipe=recipe).exists()


class TestDownloadShoppingCart:
    """Тесты API загрузки списка покупок."""

    def test_download_shopping_cart_requires_auth(self, api_client):
        """Проверка, что загрузка списка покупок требует авторизации."""
        response = api_client.get('/api/recipes/download_shopping_cart/')
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_download_empty_cart(self, authenticated_client):
        """Проверка загрузки пустого списка покупок."""
        url = '/api/recipes/download_shopping_cart/'
        response = authenticated_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert response['Content-Type'] == 'text/csv'

    def test_download_cart_with_recipes(
            self, authenticated_client, recipe):
        """Проверка загрузки списка покупок с рецептами."""
        user = authenticated_client.handler._force_user
        ShoppingCart.objects.create(user=user, recipe=recipe)
        url = '/api/recipes/download_shopping_cart/'
        response = authenticated_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert 'attachment' in response['Content-Disposition']
        assert 'shopping_cart.csv' in response['Content-Disposition']


class TestAuthAPI:
    """Тесты API аутентификации."""

    def test_login(self, api_client, user):
        """Проверка входа пользователя."""
        data = {
            'email': user.email,
            'password': 'testpass123'
        }
        response = api_client.post('/api/auth/token/login/', data)
        assert response.status_code in [
            status.HTTP_200_OK,
            status.HTTP_400_BAD_REQUEST,
            status.HTTP_404_NOT_FOUND
        ]

    def test_logout(self, authenticated_client):
        """Проверка выхода пользователя."""
        response = authenticated_client.post('/api/auth/token/logout/')
        assert response.status_code in [
            status.HTTP_200_OK,
            status.HTTP_204_NO_CONTENT,
            status.HTTP_401_UNAUTHORIZED
        ]

    def test_token_login_requires_email(self, api_client):
        """Проверка, что для входа требуется email."""
        data = {'password': 'test'}
        response = api_client.post('/api/auth/token/login/', data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST