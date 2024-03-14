import csv
from django.http import HttpResponse
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet

from .models import (Ingredient,
                     Recipe,
                     Tag,
                     IngredientInRecipe,
                     RecipesFavorite,
                     ShoppingCart
                     )
from api.filters import IngredientSearchFilter, RecipeFilter
from api.pagination import CustomPagination
from api.permissions import IsAuthorOrReadOnly
from api.serializers import (IngredientSerializer,
                             TagSerializer,
                             RecipeSerializer,
                             RecipeListSerializer,
                             FavoriteSerializer,
                             ShortRecipeSerializer,
                             ShoppingCartSerializer
                             )


class TagsViewSet(ReadOnlyModelViewSet):
    """
    Класс отображения для работы с тегами.
    Добавить тег может администратор.
    """
    queryset = Tag.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = TagSerializer


class IngredientsViewSet(ReadOnlyModelViewSet):
    """
    Класс отображения для работы с ингредиентами.
    Добавить ингредиент может администратор.
    """
    queryset = Ingredient.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = IngredientSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = IngredientSearchFilter


class RecipeViewSet(ModelViewSet):
    """
    Класс отображения для работы с рецептами.
    Для анонимов разрешен только просмотр рецептов.
    """
    queryset = Recipe.objects.all()
    permission_classes = [IsAuthorOrReadOnly]
    filter_backends = [DjangoFilterBackend]
    filterset_class = RecipeFilter
    pagination_class = CustomPagination

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

    @shopping_cart.mapping.delete
    def delete_shopping_cart(self, request, pk):
        """Удаление рецепта из корзины покупок."""
        return self.delete_method_for_actions(
            request=request, pk=pk, model=ShoppingCart)

    @action(detail=False, methods=['GET'],
            permission_classes=[IsAuthenticated])
    def download_shopping_cart(self, request):
        """Загрузка списка покупок в виде CSV файла."""
        user = self.request.user
        shopping_cart_items = ShoppingCart.objects.filter(user=user)
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = ('attachment; '
                                           'filename="shopping_cart.csv"')
        writer = csv.writer(response)
        ingredient_dict = {}

        for item in shopping_cart_items:
            recipe = item.recipe
            ingredients_in_recipe = IngredientInRecipe.objects.filter(recipe=recipe)
            for ingredient_in_recipe in ingredients_in_recipe:
                ingredient_name = ingredient_in_recipe.ingredient.name
                amount = ingredient_in_recipe.amount
                if ingredient_name in ingredient_dict:
                    ingredient_dict[ingredient_name] += amount
                else:
                    ingredient_dict[ingredient_name] = amount

        writer.writerow(['Ингредиент', 'Количество', 'Единицы измерения'])
        for ingredient_name, amount in ingredient_dict.items():
            ingredient = Ingredient.objects.get(name=ingredient_name)
            writer.writerow([
                ingredient_name,
                amount,
                ingredient.measurement_unit,
            ])

        return response
