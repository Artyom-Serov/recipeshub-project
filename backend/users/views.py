from django.db.models import Subquery
from djoser.views import UserViewSet, TokenCreateView, TokenDestroyView
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.generics import (RetrieveAPIView,
                                     get_object_or_404)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Follow, User
from api.pagination import CustomPagination
from api.serializers import (CustomUserSerializer,
                             FollowSerializer)


class CustomUserViewSet(UserViewSet, RetrieveAPIView):
    """
    Класс представления для работы с пользователями.
    """

    queryset = User.objects.all()
    serializer_class = CustomUserSerializer
    pagination_class = CustomPagination

    def list(self, request, *args, **kwargs):
        """Метод для обработки запроса списка пользователей."""
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        serializer = self.get_serializer(page, many=True)
        count = self.queryset.count()
        data = {
            'count': count,
            'next': self.paginator.get_next_link(),
            'previous': self.paginator.get_previous_link(),
            'results': serializer.data
        }
        return Response(data)

    def get(self, request, *args, **kwargs):
        """Метод получения данных о текущем пользователе."""
        serializer = self.get_serializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def retrieve(self, request, *args, **kwargs):
        """Метод получения данных о пользователе по id."""
        self.permission_classes = []
        instance = self.get_object()
        self.check_object_permissions(request, instance)
        serializer = self.get_serializer(instance)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['POST'],
            permission_classes=(IsAuthenticated,))
    def set_password(self, request):
        """Метод изменения пароля текущего пользователя."""
        user = self.request.user
        new_password = request.data.get('new_password')

        if not new_password:
            raise ValidationError({'detail': 'Новый пароль не предоставлен.'})

        user.set_password(new_password)
        user.save()

        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=True, methods=['GET', 'POST', 'DELETE'],
            permission_classes=(IsAuthenticated,))
    def subscribe(self, request, id):
        """Метод добавления или удаления подписки."""
        user = request.user
        author = get_object_or_404(User, pk=id)

        if request.method == 'GET':
            serializer = self.get_serializer(author)
            data = serializer.data
            data['is_subscribed'] = Follow.objects.filter(
                user=user, author=author).exists()
            return Response(data, status=status.HTTP_200_OK)

        if request.method == 'POST':
            serializer = FollowSerializer(
                author, data=request.data, context={'request': request}
            )
            serializer.is_valid(raise_exception=True)
            Follow.objects.create(user=request.user, author=author)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        if request.method == 'DELETE':
            get_object_or_404(
                Follow, user=user, author=author
            ).delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=False, methods=['GET'],
            permission_classes=(IsAuthenticated,))
    def subscriptions(self, request, *args, **kwargs):
        """Метод для получения пользователей,
            на которых подписан текущий пользователь."""
        user_followers = Follow.objects.filter(
            user=request.user).values('author')
        page = self.paginate_queryset(
            User.objects.filter(pk__in=Subquery(user_followers)))
        serializer = CustomUserSerializer(
            page, many=True, context={'request': request}
        )
        count = User.objects.filter(
            pk__in=Subquery(user_followers)).count()
        data = {
            'count': count,
            'next': self.paginator.get_next_link(),
            'previous': self.paginator.get_previous_link(),
            'results': serializer.data
        }
        return Response(data, status=status.HTTP_200_OK)


class CustomTokenCreateView(TokenCreateView):
    """
    Класс представления для создания токена авторизации.
    """

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        if response.status_code == status.HTTP_200_OK:
            data = {'auth_token': response.data['auth_token']}
            return Response(data, status=status.HTTP_201_CREATED)
        return response


class CustomTokenDestroyView(TokenDestroyView):
    """
    Класс представления для удаления токена авторизации.
    """

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        if response.status_code == status.HTTP_204_NO_CONTENT:
            return Response({}, status=status.HTTP_204_NO_CONTENT)
        return response
