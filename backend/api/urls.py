from django.urls import include, path
from rest_framework.routers import DefaultRouter
# from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView

from .views import (IngredientsViewSet, RecipeViewSet, TagsViewSet)
from users.views import (CustomUserViewSet, FollowListView, FollowViewSet,
                         TokenLoginView,TokenLogoutView)

router = DefaultRouter()
router.register('users', CustomUserViewSet, basename='users')
router.register('recipes', RecipeViewSet, basename='recipes')
router.register('ingredients', IngredientsViewSet, basename='ingredients')
router.register('tags', TagsViewSet, basename='tags')

user_urls = [
    # path('me/', CurrentUserView.as_view(), name='current-user'),
    path('subscriptions/', FollowListView.as_view(), name='subscriptions'),
    path('<int:user_id>/subscribe/',
         FollowViewSet.as_view(),
         name='subscribe'),
]

urlpatterns = [
    path('', include(router.urls)),
    path('users/', include(user_urls)),
    path('users/subscriptions/', FollowListView.as_view(), name='subscriptions'),
    path('', include('djoser.urls')),
    path('auth/token/login/', TokenLoginView.as_view(), name='token_login'),
    path('auth/token/logout/', TokenLogoutView.as_view(), name='token_logout'),
    # path('auth/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    # path('auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    # path('auth/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    # path('auth/', include('djoser.urls.authtoken')),
]
