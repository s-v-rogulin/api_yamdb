from django.urls import include, path
from rest_framework.routers import DefaultRouter

app_name = 'API'

v1_router = DefaultRouter()
v1_router.register('genres', PostViewSet, basename='genres')
v1_router.register('categories', GroupViewSet, basename='categories')
v1_router.register('titles', GroupViewSet, basename='titles')
v1_router.register('users',GroupViewSet, basename='users')
v1_router.register(
    r'^titles/(?P<title_id>\d+)/reviews',
    CommentViewSet,
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
