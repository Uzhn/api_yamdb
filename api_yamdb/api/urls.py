from django.urls import path, include

from rest_framework.routers import DefaultRouter

from api.views import (UserViewSet, user_registration, get_token_for_user,
                       TitleViewSet, GenreViewSet, CategoryViewSet,
                       ReviewsViewSet, CommentViewSet,
                       )


app_name = 'api'

router = DefaultRouter()
router.register('users', UserViewSet, basename='user')
router.register('titles', TitleViewSet)
router.register('genres', GenreViewSet)
router.register('categories', CategoryViewSet)
router.register('titles/(?P<title_id>[\d]{1,})/reviews',
                ReviewsViewSet, basename='reviews'
                )
router.register(
    r'titles/(?P<title_id>[\d]{1,})/reviews/(?P<review_id>[\d]{1,})/comments',
    CommentViewSet, basename='comments'
)


urlpatterns = [
    path('', include(router.urls)),
    path('auth/signup/', user_registration),
    path('auth/token/', get_token_for_user),
]
