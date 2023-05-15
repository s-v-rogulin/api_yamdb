from django.urls import include, path
from rest_framework.routers import DefaultRouter
from api.views import (CategoryViewSet, CommentViewSet, GenreViewSet,
                       ReviewViewSet, TitleViewSet, UserViewSet)
app_name = 'API'

v1_router = DefaultRouter()
v1_router.register('genres', GenreViewSet, basename='genres')
v1_router.register('categories', CategoryViewSet, basename='categories')
v1_router.register('titles', TitleViewSet, basename='titles')
v1_router.register('users',UserViewSet, basename='users')
v1_router.register(
    r'^titles/(?P<title_id>\d+)/reviews',
    ReviewViewSet,
    basename='reviews'
)
v1_router.register(
    r'^titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet,
    basename='comments'
)

urlpatterns = [
    path('v1/auth/', include([
        path('signup/', ConfCodeView.as_view()),
        path('token/', TokenView.as_view())
    ])),
    path('v1/', include(router_v1.urls)),
]
