"""Fixtures for API clients."""
import pytest


@pytest.fixture
def api_client():
    """Создание API-клиента."""
    from rest_framework.test import APIClient
    return APIClient()


@pytest.fixture
def authenticated_client(api_client, user):
    """Создание авторизованного API-клиента."""
    api_client.force_authenticate(user=user)
    return api_client
