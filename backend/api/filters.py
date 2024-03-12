from django_filters.rest_framework import FilterSet, filters
from django_filters import rest_framework as django_filters


from recipes.models import Recipe, Ingredient, Tag


class IngredientSearchFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(
        field_name='name', lookup_expr='icontains')
    """
    Фильтр для поиска ингредиентов по имени.
    """

    class Meta:
        model = Ingredient
        fields = ['name']


class RecipeFilter(FilterSet):
    """
    Фильтры для сортировки рецептов по тегам, наличию в избранном
    и наличию в корзине.
    """

    tags = filters.ModelMultipleChoiceFilter(
        field_name='tags__slug',
        to_field_name='slug',
        queryset=Tag.objects.all(),
    )

    is_favorited = filters.BooleanFilter(method='filter_is_favorited')
    is_in_shopping_cart = filters.BooleanFilter(
        method='filter_is_in_shopping_cart'
    )

    class Meta:
        model = Recipe
        fields = ('tags', 'author', 'is_favorited', 'is_in_shopping_cart')

    def filter_is_favorited(self, queryset, name, value):
        if value:
            return queryset.filter(favorites__user=self.request.user)
        return queryset

    def filter_is_in_shopping_cart(self, queryset, name, value):
        if value:
            return queryset.filter(carts__user=self.request.user)
        return queryset
