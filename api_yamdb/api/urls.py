from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (
    CategoryViewSet, CommentViewSet, GenreViewSet,
    ReviewVeiwSet, SignUpView, TitleViewSet, TokenView,
    UsersViewSet
)

router_v1 = DefaultRouter()
router_v1.register('users', UsersViewSet, basename='users')
router_v1.register(
    r'titles/(?P<title_id>[\d]+)/reviews(?P<review_id>[\d]*)',
    ReviewVeiwSet, basename='reviews'
)
router_v1.register(
    r'titles/(?P<title_id>[\d]+)/reviews/(?P<review_id>[\d]+)/'
    r'comments(?P<comment_id>[\d]*)',
    CommentViewSet, basename='comments'
)
router_v1.register('titles', TitleViewSet, basename='titles')
router_v1.register('categories', CategoryViewSet, basename='categories')
router_v1.register('genres', GenreViewSet, basename='genres')
urlpatterns = [
    path('v1/', include(router_v1.urls)),
    path('v1/auth/signup/', SignUpView.as_view(), name='SignUp'),
    path('v1/auth/token/', TokenView.as_view(), name='Token')
]
