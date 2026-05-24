"""Конфигурация pytest"""
import shutil
from pathlib import Path

import pytest

pytest_plugins = [
    'tests.fixtures.fixture_clients',
    'tests.fixtures.fixture_recipes',
    'tests.fixtures.fixture_users',
]

pytestmark = pytest.mark.django_db

@pytest.fixture(autouse=True)
def cleanup_media_files():
    """Очистка медиафайлов после каждого теста."""
    yield
    media_dir = Path(__file__).resolve().parent.parent / 'media'
    if media_dir.exists():
        for items in media_dir.iterdir():
            if items.is_file():
                items.unlink()
            elif items.is_dir():
                shutil.rmtree(items)

@pytest.fixture
def test_image_base64():
     """Фикстура тестового изображения."""
     b64 = 'iVBORw0KGgoAAAANSUhEUgAAAAoAAAAKCAYAAACNMs+9AAAAGElEQ'
     b64 += 'VR4nGP8z8Dwn4EIwESMolGF1FMIAD2cAhK2AyPVAAAAAElFTkSuQmCC'
     return b64
