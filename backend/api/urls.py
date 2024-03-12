from django.urls import include, path, re_path
from rest_framework.routers import DefaultRouter
from recipes.views import (IngredientsViewSet,
                           RecipeViewSet,
                           TagsViewSet,
                           ShoppingCartViewSet
                           )
from users.views import CustomUserViewSet

app_name = 'api'

router = DefaultRouter()
router.register('users', CustomUserViewSet, basename='users')
router.register('recipes', RecipeViewSet, basename='recipes')
router.register('ingredients', IngredientsViewSet, basename='ingredients')
router.register('tags', TagsViewSet, basename='tags')

urlpatterns = [
    path('', include(router.urls)),
    path('recipes/download_shopping_cart/',
         ShoppingCartViewSet.as_view(),
         name='download_shopping_cart'),
    path('drf-auth/', include('rest_framework.urls')),
    path('auth/', include('djoser.urls')),
    re_path(r'^auth/', include('djoser.urls.authtoken')),
]
