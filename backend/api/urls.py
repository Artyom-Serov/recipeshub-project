from django.urls import include, path
from rest_framework.routers import DefaultRouter
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from recipes.views import (IngredientsViewSet, RecipeViewSet, TagsViewSet)
from users.views import (CustomUserViewSet, CustomTokenCreateView,
                         CustomTokenDestroyView)

router = DefaultRouter()
router.register('users', CustomUserViewSet, basename='users')
router.register('recipes', RecipeViewSet, basename='recipes')
router.register('ingredients', IngredientsViewSet, basename='ingredients')
router.register('tags', TagsViewSet, basename='tags')

schema_view = get_schema_view(
    openapi.Info(
        title="API for project foodgramm",
        default_version='v1',
        # description="Your project API description",
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)
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
    path('docs/', schema_view.with_ui(
        'redoc', cache_timeout=0), name='schema-redoc'),
]
