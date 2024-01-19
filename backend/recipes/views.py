from django.http import HttpResponse
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet

from recipes.models import (Ingredient, Recipe,
                            Tag, RecipesFavorite, ShoppingCart,
                            IngredientInRecipe)
from .filters import IngredientSearchFilter, RecipeFilter
from .pagination import CustomPagination
from .permissions import IsAuthorOrReadOnly
from .serializers import (IngredientSerializer,
                          TagSerializer,
                          RecipeSerializer,
                          RecipeListSerializer,
                          FavoriteSerializer,
                          ShoppingCartSerializer)


class TagsViewSet(ReadOnlyModelViewSet):
    """
    ViewSet для работы с тегами.
    Добавить тег может администратор.
    """
    queryset = Tag.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = TagSerializer


class IngredientsViewSet(ReadOnlyModelViewSet):
    """
    ViewSet для работы с ингредиентами.
    Добавить ингредиент может администратор.
    """
    queryset = Ingredient.objects.all()
    permission_classes = (AllowAny, )
    filter_backends = [IngredientSearchFilter]
    serializer_class = IngredientSerializer
    search_fields = ('^name',)


class RecipeViewSet(ModelViewSet):
    """
    ViewSet для работы с рецептами.
    Для анонимов разрешен только просмотр рецептов.
    """
    queryset = Recipe.objects.all()
    permission_classes = [IsAuthorOrReadOnly]
    filter_backends = [DjangoFilterBackend]
    filterset_class = RecipeFilter
    pagination_class = CustomPagination
    serializer_class = RecipeSerializer

    def get_serializer_class(self):
        """Получение класса сериализатора в зависимости от действия."""
        if self.action in ('list', 'retrieve'):
            return RecipeListSerializer
        return RecipeSerializer

    @staticmethod
    def post_method_for_actions(request, pk, serializers):
        """Общий метод для обработки POST-запросов."""
        data = {'user': request.user.id, 'recipe': pk}
        serializer = serializers(data=data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @staticmethod
    def delete_method_for_actions(request, pk, model):
        """Общий метод для обработки DELETE-запросов."""
        user = request.user
        recipe = get_object_or_404(Recipe, id=pk)
        model_obj = get_object_or_404(model, user=user, recipe=recipe)
        model_obj.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=True, methods=['POST'],
            permission_classes=[IsAuthenticated])
    def favorite(self, request, pk):
        """Добавление рецепта в избранное."""
        return self.post_method_for_actions(
            request=request, pk=pk, serializers=FavoriteSerializer)

    @favorite.mapping.delete
    def delete_favorite(self, request, pk):
        """Удаление рецепта из избранного."""
        return self.delete_method_for_actions(
            request=request, pk=pk, model=RecipesFavorite)

    @action(detail=True, methods=['POST'],
            permission_classes=[IsAuthenticated])
    def shopping_cart(self, request, pk):
        """Добавление рецепта в корзину покупок."""
        return self.post_method_for_actions(
            request=request, pk=pk, serializers=ShoppingCartSerializer)

    @action(detail=False, methods=['GET'],
            permission_classes=[IsAuthenticated])
    def download_shopping_cart(self, request):
        """Загрузка списка покупок в виде текстового файла."""
        user = self.request.user
        shopping_cart_items = ShoppingCart.objects.filter(user=user)
        file = "Shopping Cart:\n\n"
        for item in shopping_cart_items:
            recipe = item.recipe
            ingredients = recipe.ingredients.all()
            file += f"Recipe: {recipe.title}\n"
            for ingredient in ingredients:
                file += f"{ingredient.name}: {item.amount} {ingredient.unit}\n"
            file += "\n"
        response = HttpResponse(file, content_type='text/plain')
        response['Content-Disposition'] = ('attachment; '
                                           'filename="shopping_cart.txt"')
        return response

    @shopping_cart.mapping.delete
    def delete_shopping_cart(self, request, pk):
        """Удаление рецепта из корзины покупок."""
        return self.delete_method_for_actions(
            request=request, pk=pk, model=ShoppingCart)
