from django.urls import include, path
from rest_framework.routers import DefaultRouter

from recipes.views import (IngredientsViewSet, RecipeViewSet, TagsViewSet)
from users.views import (CustomUserViewSet, CustomTokenCreateView,
                         CustomTokenDestroyView)

router = DefaultRouter()
router.register('users', CustomUserViewSet, basename='users')
router.register('recipes', RecipeViewSet, basename='recipes')
router.register('ingredients', IngredientsViewSet, basename='ingredients')
router.register('tags', TagsViewSet, basename='tags')

urlpatterns = [
    path('', include(router.urls)),
    path('api/', include('djoser.urls')),
    path('drf-auth/', include('rest_framework.urls')),
    path(
        'auth/token/login/',
        CustomTokenCreateView.as_view(),
        name='token_create'),
    path(
        'auth/token/logout/',
        CustomTokenDestroyView.as_view(),
        name='token_destroy'),
]
