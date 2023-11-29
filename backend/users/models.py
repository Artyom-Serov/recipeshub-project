from django.contrib.auth.models import (AbstractBaseUser, BaseUserManager,
                                        PermissionsMixin)
from django.db import models


class CustomUserManager(BaseUserManager):
    """Кастомный менеджер пользователей.

    Определяет методы для создания обычного пользователя (`create_user`) и
    суперпользователя (`create_superuser`).
    """
    def create_user(self, email, username, first_name, last_name,
                    password=None, **extra_fields):
        """
        Создание и сохранение пользователя с адресом
        электронной почты и паролем.
        """
        if not email:
            raise ValueError('Указание электронной почты обязательным')
        email = self.normalize_email(email)
        user = self.model(email=email, username=username,
                          first_name=first_name, last_name=last_name,
                          **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, first_name, last_name,
                         password=None, **extra_fields):
        """
        Создание и сохранение суперпользователя с адресом
        электронной почты и паролем.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(
                'Суперпользователь должен иметь атрибут is_staff=True.'
            )
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(
                'Суперпользователь должен иметь атрибут is_superuser=True.'
            )

        return self.create_user(email, username, first_name, last_name,
                                password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    """Модель пользователя."""

    email = models.EmailField(
        'Адрес электронной почты',
        unique=True,
        max_length=150,
    )
    username = models.CharField(
        'Уникальный юзернейм',
        max_length=150,
        unique=True,
    )
    first_name = models.CharField('Имя', max_length=150)
    last_name = models.CharField('Фамилия', max_length=150)
    is_active = models.BooleanField('Активирован', default=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ['id']

    def get_full_name(self):
        return f'{self.first_name} {self.last_name}'

    def __str__(self):
        return self.email


class Follow(models.Model):
    """Модель подписки."""

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='follower',
        verbose_name='Подписчик',
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='following',
        verbose_name='Автор',
    )

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'author'],
                name='unique follow',
            )
        ]
