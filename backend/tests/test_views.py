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
