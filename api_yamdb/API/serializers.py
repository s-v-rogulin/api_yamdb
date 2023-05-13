from django.contrib.auth import get_user_model
from django.conf import settings
from django.core.validators import MinValueValidator
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from reviews.models import Genre, Category, Title, Review, Comment
from .mixins import UsernameSerializer
from reviews.validators import validate_year
from users.models import User

User = get_user_model()


class Genreserializer(serializers.ModelSerializer):

    class Meta:
        model = Genre
        fields = ('name', 'slug')


class Categoryserializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ('name', 'slug')


class TitleSerializer(serializers.ModelSerializer):
    genre = GenreSerializer(many=True)
    category = CategorySerializer()
    rating = serializers.IntegerField(default=1)
    year = serializers.IntegerField(validators=[MinValueValidator(0),
                                                validate_year, ])

    class Meta:
        fields = (
            'id', 'name', 'year', 'rating', 'description', 'genre', 'category')
        model = Title
        read_only_fields = (
            'id', 'name', 'year', 'rating', 'description', 'genre', 'category')


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
        read_only=True,
    )

    class Meta:
        model = Comment
        fields = ('id', 'text', 'author', 'pub_date')
        read_only = ('id',)



class SignUpSerializer(serializers.Serializer, UsernameSerializer):
    username = serializers.CharField(
        max_length=settings.LIMIT_USERNAME,
        required=True)
    email = serializers.EmailField(
        max_length=settings.LIMIT_EMAIL,
        required=True)
    

class TokenSerializer(serializers.Serializer, UsernameSerializer):
    username = serializers.CharField(
        max_length=settings.LIMIT_USERNAME,
        required=True)
    confirmation_code = serializers.CharField(
        max_length=settings.LIMIT_CONF_CODE,
        required=True)


class UserSerializer(serializers.ModelSerializer, UsernameSerializer):
    username = serializers.CharField(
        max_length=settings.LIMIT_USERNAME,
        validators=[UniqueValidator(queryset=User.objects.all()), ],
        required=True)
    email = serializers.EmailField(
        max_length=settings.LIMIT_EMAIL,
        validators=[UniqueValidator(queryset=User.objects.all()), ],
        required=True)

    class Meta:
        model = User
        fields = ('username',
                  'email',
                  'first_name',
                  'last_name',
                  'bio',
                  'role')
        

class NotAdminUserSerializer(UserSerializer, UsernameSerializer):
    class Meta(UserSerializer.Meta):
        read_only_fields = ('role',)


class TitlePostSerialzier(serializers.ModelSerializer):
    """Сериализатор для POST, PATCH, PUT произведения."""
    genre = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Genre.objects.all(),
        many=True
    )
    category = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Category.objects.all()
    )
    rating = serializers.IntegerField(required=False)
    year = serializers.IntegerField(validators=[MinValueValidator(0),
                                                validate_year, ])

    class Meta:
        model = Title
        fields = (
            'id', 'name', 'year', 'rating', 'description', 'genre', 'category')

    def to_representation(self, instance):
        return TitleSerializer(instance).data
