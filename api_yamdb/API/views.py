from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404
from reviews.models import Genre, Category, Title, Review, Comment
from users.models import User
from .permissions import AdminOrReadOnly, IsStaffOrAuthorOrReadOnly, IsRoleAdmin
from rest_framework import viewsets

from .serializers import Genreserializer, Categoryserializer, Titleserializer, Reviewserializer, Commentserializer, Userserializer


class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all
    serializer_class = Genreserializer
    permission_classes = (AdminOrReadOnly,)


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all
    serializer_class = Categoryserializer
    permission_classes = (AdminOrReadOnly,)


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all
    serializer_class = Titleserializer
    permission_classes = (AdminOrReadOnly,)


class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all
    serializer_class = Reviewserializer
    permission_classes = IsStaffOrAuthorOrReadOnly

    def get_queryset(self):
        title_id = self.kwargs.get('title_id')
        title = get_object_or_404(Title, id=title_id)
        return title.reviews.all()

    def perform_create(self, serializer):
        title_id = self.kwargs.get('title_id')
        title = get_object_or_404(Title, id=title_id)
        serializer.save(author=self.request.user, title=title)


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all
    serializer_class = Commentserializer
    permission_classes = IsStaffOrAuthorOrReadOnly

    def get_queryset(self):
        review = get_object_or_404(Review, id=self.kwargs.get('review_id'))
        return review.comments.all()

    def perform_create(self, serializer):
        review = get_object_or_404(Review, id=self.kwargs.get('review_id'))
        serializer.save(author=self.request.user,
                        review=review)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all
    serializer_class = Userserializer
    permission_classes = (AdminOrReadOnly,)
