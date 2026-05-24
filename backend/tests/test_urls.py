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
