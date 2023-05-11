from django.contrib.auth import get_user_model
from reviews.models import Genre, Category, Title, Review, Comment
from users.models import User
from rest_framework import serializers

User = get_user_model()


class Genreserializer(serializers.ModelSerializer):

    class Meta:
        model = Genre
        fields = ('name', 'slug')


class Categoryserializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ('name', 'slug')

class Titleserializer(serializers.ModelSerializer):

    class Meta:


class Reviewserializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username', read_only=True,)
    score = serializers.IntegerField(max_value=10, min_value=1)

    class Meta:
        model = Review
        fields = ('id', 'text', 'author', 'score', 'pub_date')
        read_only = ('id',)


class Commentserializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True,)

    class Meta:
        model = Comment
        fields = ('id', 'text', 'author', 'pub_date')
        read_only = ('id',)


class Userserializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('username', 'email', 'bio', 'role')