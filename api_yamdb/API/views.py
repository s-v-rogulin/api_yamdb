from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404
from reviews.models import Genre, Category, Title, Review, Comment
from users.models import User

from rest_framework import viewsets

from .serializers import Genreserializer, Categoryserializer, Titleserializer, Reviewserializer, Commentserializer, Userserializer


class Genre():
    queryset = Genre.objects.all
    serializer_class = Genreserializer
    permission_classes = (AdminOrReadOnly,)

class Category():
    queryset = Category.objects.all
    serializer_class = Categoryserializer
    permission_classes = (AdminOrReadOnly,)

class Title():
    queryset = Title.objects.all
    serializer_class = Titleserializer
    permission_classes = (AdminOrReadOnly,)

class Review():
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



class Comment():
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

class User():
    queryset = User.objects.all
    serializer_class = Userserializer
    permission_classes = (AdminOrReadOnly,)
