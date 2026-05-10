"""Конфигурация pytest"""
import pytest

pytest_plugins = [
#    'tests.fixtures.fixture_clients',
    'tests.fixtures.fixture_recipes',
    'tests.fixtures.fixture_users',
]

pytestmark = pytest.mark.django_db

@pytest.fixture
def test_image_base64():
     """Фикстура тестового изображения."""
     b64 = 'iVBORw0KGgoAAAANSUhEUgAAAAoAAAAKCAYAAACNMs+9AAAAGElEQ'
     b64 += 'VR4nGP8z8Dwn4EIwESMolGF1FMIAD2cAhK2AyPVAAAAAElFTkSuQmCC'
     return b64
