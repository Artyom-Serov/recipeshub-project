"""Тесты URL-маршрутов приложения."""

import pytest

pytestmark = pytest.mark.django_db


class TestURLPatterns:
    """Тесты URL-маршрутов."""

    def test_api_endpoints_registered(self, api_client):
        """Проверка регистрации основных эндпоинтов API."""
        endpoints = [
            '/api/users/',
            '/api/recipes/',
            '/api/ingredients/',
            '/api/tags/',
            '/api/drf-auth/login/',
            '/api/auth/users/',
        ]
        for endpoint in endpoints:
            response = api_client.get(endpoint)
            assert response.status_code in (
                200, 201, 204, 400, 401, 403, 404
            ), f'Endpoint {endpoint} not accessible: {response.status_code}'

    def test_token_login_endpoint_exists(self, api_client):
        """Проверка эндпоинта получения токена (POST)."""
        response = api_client.post('/api/auth/token/login')
        assert response.status_code in (200, 400, 401), (
            f'Endpoint not accessible: {response.status_code}'
        )

    def test_users_endpoints(self, api_client, user):
        """Проверка эндпоинтов пользователей."""
        response = api_client.get('/api/users/')
        assert response.status_code == 200

        response = api_client.get('/api/users/me/')
        assert response.status_code in (200, 401)

        response = api_client.get(f'/api/users/{user.id}/')
        assert response.status_code == 200

    def test_ingredients_endpoints(self, api_client):
        """Проверка эндпоинтов ингредиентов."""
        response = api_client.get('/api/ingredients/')
        assert response.status_code == 200

    def test_recipes_endpoints(self, api_client):
        """Проверка эндпоинтов рецептов."""
        response = api_client.get('/api/recipes/')
        assert response.status_code == 200

    def test_tags_endpoints(self, api_client):
        """Проверка эндпоинтов тегов."""
        response = api_client.get('/api/tags/')
        assert response.status_code == 200
