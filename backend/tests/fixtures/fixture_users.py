"""Fixtures for users."""
import pytest


@pytest.fixture
def user(db):
    """Создание тестового пользователя."""
    from users.models import User
    return User.objects.create_user(
        email='test@test.com',
        username='testuser',
        first_name='Test',
        last_name='User',
        password='testpass123'
    )


@pytest.fixture
def user2(db):
    """Создание второго тестового пользователя."""
    from users.models import User
    return User.objects.create_user(
        email='test2@test.com',
        username='testuser2',
        first_name='Test2',
        last_name='User2',
        password='testpass123'
    )


@pytest.fixture
def admin_user(db):
    """Создание администратора."""
    from users.models import User
    return User.objects.create_superuser(
        email='admin@test.com',
        username='admin',
        first_name='Admin',
        last_name='User',
        password='adminpass123'
    )


@pytest.fixture
def follow(db, user, user2):
    """Создание подписки пользователя на автора."""
    from users.models import Follow
    return Follow.objects.create(user=user, author=user2)
