from djoser.views import UserViewSet
from django.core.exceptions import PermissionDenied
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.generics import (ListAPIView, RetrieveAPIView,
                                     get_object_or_404)
from rest_framework.permissions import (IsAuthenticated, AllowAny,
                                        IsAuthenticatedOrReadOnly)
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView

from .models import Follow, User
from api.pagination import CustomPagination
from api.serializers import (CustomUserSerializer,
                             FollowSerializer)


class CustomUserViewSet(UserViewSet, RetrieveAPIView):
    """
    ViewSet для работы с пользователями.
    """

    queryset = User.objects.all()
    serializer_class = CustomUserSerializer
    # permission_classes = [IsAuthenticated]
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

    # @action(detail=False, methods=['GET'])
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

    # @action(detail=False, methods=['POST'])
    # def login(self, request):
    #     """
    #     Метод для получения токена авторизации.
    #     """
    #     serializer = TokenObtainPairSerializer(data=request.data)
    #     serializer.is_valid(raise_exception=True)
    #     return Response(serializer.validated_data, status=status.HTTP_201_CREATED)

    # @action(detail=False, methods=['POST'], permission_classes=[IsAuthenticated])
    # def logout(self, request):
    #     """
    #     Метод для удаления токена текущего пользователя.
    #     """
    #     # Используйте методы из rest_framework_simplejwt для разрушения токена
    #     refresh_token = request.data.get('refresh')
    #     if refresh_token:
    #         RefreshToken(refresh_token).blacklist()
    #         return Response(status=status.HTTP_204_NO_CONTENT)
    #     else:
    #         return Response({'detail': 'Не предоставлен refresh токен.'},
    #                         status=status.HTTP_400_BAD_REQUEST)


class TokenLoginView(TokenObtainPairView):
    """
    Класс для получения токена авторизации.
    """
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data.get('id')
        refresh = RefreshToken.for_user(user)
        return Response(
            {'auth_token': str(refresh.access_token)},
            status=status.HTTP_201_CREATED)


class TokenLogoutView(APIView):
    """
    Класс для удаления токена.
    """
    def post(self, request, *args, **kwargs):
        refresh_token = request.data.get('refresh_token')

        if not refresh_token:
            return Response(
                {'detail': 'Refresh token не предоставлен.'},
                status=status.HTTP_400_BAD_REQUEST)

        try:
            RefreshToken(refresh_token).blacklist()
        except Exception:
            return Response(
                {'detail': 'Неверный refresh token.'},
                status=status.HTTP_400_BAD_REQUEST)

        return Response(status=status.HTTP_204_NO_CONTENT)


# class CurrentUserView(RetrieveAPIView):
#     """
#     Представление получения информации о текущем пользователе.
#     """
#     permission_classes = [IsAuthenticated]
#     serializer_class = CustomUserSerializer
#
#     def get_object(self):
#         """Получение объекта текущего пользователя."""
#         return self.request.user
#
#     def retrieve(self, request, *args, **kwargs):
#         """Обработка GET-запроса и возврат информации о пользователе."""
#         instance = self.get_object()
#         serializer = self.get_serializer(instance)
#         return Response(serializer.data, status=status.HTTP_200_OK)
#
#     def handle_exception(self, exc):
#         """Обработка исключения для возврата описания
#         ошибки при статус-коде 401."""
#         if isinstance(exc, PermissionDenied):
#             return Response(
#                 {"detail": "Учетные данные не были предоставлены."},
#                 status=status.HTTP_401_UNAUTHORIZED
#             )
#         return super().handle_exception(exc)


class FollowViewSet(APIView):
    """
    APIView для добавления и удаления подписки на автора
    """

    serializer_class = FollowSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = CustomPagination

    def post(self, request, *args, **kwargs):
        """Метод для добавления подписки на автора."""
        user_id = self.kwargs.get('user_id')
        if user_id == request.user.id:
            return Response(
                {'error': 'Нельзя подписаться на себя'},
                status=status.HTTP_400_BAD_REQUEST
            )
        if Follow.objects.filter(
                user=request.user,
                author_id=user_id
        ).exists():
            return Response(
                {'error': 'Вы уже подписаны на пользователя'},
                status=status.HTTP_400_BAD_REQUEST
            )
        author = get_object_or_404(User, id=user_id)
        Follow.objects.create(
            user=request.user,
            author_id=user_id
        )
        return Response(
            self.serializer_class(author, context={'request': request}).data,
            status=status.HTTP_201_CREATED
        )

    def delete(self, request, *args, **kwargs):
        """Метод для удаления подписки на автора."""
        user_id = self.kwargs.get('user_id')
        get_object_or_404(User, id=user_id)
        subscription = Follow.objects.filter(
            user=request.user,
            author_id=user_id
        )
        if subscription:
            subscription.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(
            {'error': 'Вы не подписаны на пользователя'},
            status=status.HTTP_400_BAD_REQUEST
        )


class FollowListView(ListAPIView):
    """
    APIView для просмотра подписок.
    """

    serializer_class = FollowSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = CustomPagination

    def get_queryset(self):
        """Метод для получения списка подписок текущего пользователя."""
        return User.objects.filter(following__user=self.request.user)