from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import IntegrityError
from rest_framework import serializers

from reviews.models import Category, Comment, Genre, Review, Title
from users.models import User
from .validators import validate_username


class AuthSerializer(serializers.Serializer):
    username = serializers.CharField(
        required=True, max_length=150,
        validators=(validate_username, UnicodeUsernameValidator())
    )
    email = serializers.EmailField(required=True, max_length=254)

    def validate(self, data):
        try:
            User.objects.get_or_create(**data)
        except IntegrityError:
            raise serializers.ValidationError(
                'username или email уже занято'
            )
        return data


class TokenSerializer(serializers.Serializer):
    username = serializers.CharField()
    confirmation_code = serializers.CharField()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'username', 'email',
            'first_name', 'last_name',
            'role', 'bio'
        )


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True, default=serializers.CurrentUserDefault(),
        slug_field='username',
    )

    class Meta:
        model = Review
        fields = '__all__'
        read_only_fields = ('title',)

    def validate(self, data):
        if (
            self.context['request'].method == 'POST'
            and Review.objects.filter(
                title=self.context['title_id'],
                author=self.context['request'].user
            ).exists()
        ):
            raise serializers.ValidationError(
                'Вы уже оставляли отзыв на это произведение.'
            )
        return data

    def validate_score(self, value):
        if 1 <= value <= 10:
            return value
        raise serializers.ValidationError('Оценка должна быть от1 до 10.')


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True, default=serializers.CurrentUserDefault(),
        slug_field='username',
    )

    class Meta:
        model = Comment
        fields = '__all__'
        read_only_fields = ('review',)


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        exclude = ['id']


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        exclude = ['id']


class ListDetailedTitleSerializer(serializers.ModelSerializer):
    genre = GenreSerializer(many=True)
    category = CategorySerializer()
    rating = serializers.IntegerField()

    class Meta:
        model = Title
        fields = '__all__'


class TitleSerializer(serializers.ModelSerializer):
    genre = serializers.SlugRelatedField(
        slug_field='slug', many=True,
        queryset=Genre.objects.all()
    )
    category = serializers.SlugRelatedField(
        slug_field='slug', queryset=Category.objects.all()
    )

    class Meta:
        model = Title
        fields = '__all__'
