from rest_framework import routers

from django.urls import path, include

from api.views import UserViewSet, ReviewsViewSet, CommentViewSet, TitlesViewSet, GenreViewSet, CategoryViewSet, user_registration, get_token_for_user

router_api_v01 = routers.DefaultRouter()
router_api_v01.register(r'titles/(?P<title_id>[\d]{1,})/reviews',
                        ReviewsViewSet, basename='reviews')
router_api_v01.register(r'titles/(?P<title_id>[\d]{1,})/reviews/(?P<review_id>[\d]{1,})/comments',
                        CommentViewSet, basename='comments')
router_api_v01.register(r'users', UserViewSet, basename='user')
router_api_v01.register(r'titles', TitlesViewSet, basename='titles')
router_api_v01.register(r'genres', GenreViewSet)
router_api_v01.register(r'categories', CategoryViewSet)

urlpatterns = [
    path('', include(router_api_v01.urls)),
    path('auth/signup/', user_registration),
    path('auth/token/', get_token_for_user),
]
