from djoser.views import UserViewSet
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response

from .models import Follow, User
from api.pagination import CustomPagination
from api.serializers import (CustomUserSerializer,
                             FollowSerializer)


class CustomUserViewSet(UserViewSet):
    """
    Класс представления для работы с пользователями.
    """

    queryset = User.objects.all()
    serializer_class = CustomUserSerializer
    pagination_class = CustomPagination

    def get_permissions(self):
        if self.action in ['retrieve']:
            return [AllowAny()]
        return super().get_permissions()

    @action(detail=False, permission_classes=[IsAuthenticated])
    def me(self, request):
        user = request.user
        serializer = CustomUserSerializer(user, context={'request': request})
        data = serializer.data
        data['is_subscribed'] = False
        return Response(data)

    @action(
        detail=True,
        methods=['POST', 'DELETE'],
        permission_classes=[IsAuthenticated]
    )
    def subscribe(self, request, **kwargs):
        """Метод добавления или удаления подписки."""
        user = request.user
        # author_id = self.kwargs.get('pk')
        author_id = self.kwargs.get('id')
        author = get_object_or_404(User, id=author_id)

        if request.method == 'POST':
            serializer = FollowSerializer(
                author, data=request.data, context={"request": request})
            serializer.is_valid(raise_exception=True)
            Follow.objects.create(user=user, author=author)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        if request.method == 'DELETE':
            if not user.is_authenticated:
                return Response({'detail': 'Пользователь не авторизован'},
                                status=status.HTTP_401_UNAUTHORIZED)

            subscription = Follow.objects.filter(
                user=user, author=author).first()
            if not subscription:
                return Response({'detail': 'Подписка не найдена'},
                                status=status.HTTP_400_BAD_REQUEST)

            subscription.delete()
            return Response({'detail': 'Успешная отписка'},
                            status=status.HTTP_204_NO_CONTENT)

    @action(
        detail=False,
        permission_classes=[IsAuthenticated]
    )
    def subscriptions(self, request):
        """Метод для получения пользователей,
        на которых подписан текущий пользователь."""
        user = request.user
        queryset = User.objects.filter(following__user=user)
        pages = self.paginate_queryset(queryset)
        serializer = FollowSerializer(
            pages, many=True, context={'request': request})
        return self.get_paginated_response(serializer.data)
