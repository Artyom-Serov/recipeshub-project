from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (IngredientsViewSet, RecipeViewSet, TagsViewSet,
                    CustomUserViewSet, FollowListView, FollowViewSet,
                    CurrentUserView)

router = DefaultRouter()
router.register('users', CustomUserViewSet, basename='users')
router.register('recipes', RecipeViewSet, basename='recipes')
router.register('ingredients', IngredientsViewSet, basename='ingredients')
router.register('tags', TagsViewSet, basename='tags')

user_urls = [
    path('me/', CurrentUserView.as_view(), name='current-user'),
    path('subscriptions/', FollowListView.as_view(), name='subscriptions'),
    path('<int:user_id>/subscribe/',
         FollowViewSet.as_view(),
         name='subscribe'),
]

urlpatterns = [
    path('users/', include(user_urls)),
    path('', include(router.urls)),
    path('', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
]
