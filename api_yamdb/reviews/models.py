from django.core.validators import MaxValueValidator, MinValueValidator
from django.db.models import (
    CASCADE, SET_NULL, CharField, DateTimeField,
    ForeignKey, ManyToManyField, Model, PositiveIntegerField,
    SlugField, TextField, UniqueConstraint,
)
from django.utils import timezone

from .validators import year_validator
from users.models import User


class Genre(Model):
    name = CharField(
        'Название жанра',
        max_length=256,
    )
    slug = SlugField(
        unique=True,
        max_length=50,
    )

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'
        ordering = ('name',)

    def __str__(self):
        return self.name[:40]


class Category(Model):
    name = CharField(
        'Название категории',
        max_length=256,
    )
    slug = SlugField(
        unique=True,
        max_length=50,
    )

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ('name',)

    def __str__(self):
        return self.name[:40]


class Title(Model):
    name = CharField(
        'Название произведения',
        max_length=256,
    )
    description = TextField(
        'Описание произведения',
        null=True,
        blank=True,
    )
    year = PositiveIntegerField(
        'Год выхода',
        validators=(year_validator,),
    )
    genre = ManyToManyField(
        Genre,
        related_name='titles',
        verbose_name='Жанр произведения',
    )
    category = ForeignKey(
        Category,
        related_name='titles',
        on_delete=SET_NULL,
        null=True,
        blank=True,
        verbose_name='Категория произведения',
    )

    class Meta:
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'
        ordering = ('year',)

    def __str__(self):
        return self.name[:40]


class Review(Model):
    title = ForeignKey(
        Title,
        related_name='reviews',
        on_delete=CASCADE,
        verbose_name='Название произведения',
    )
    text = TextField('Текст отзыва',)
    author = ForeignKey(
        User,
        related_name='reviews',
        on_delete=CASCADE,
        verbose_name='Автор отзыва',
    )
    score = PositiveIntegerField(
        'Рейтинг',
        validators=(
            MinValueValidator(1, 'Минимальная оценка - 1'),
            MaxValueValidator(10, 'Максимальная оценка - 10')
        ),
    )
    pub_date = DateTimeField(
        'Дата публикации отзыва',
        default=timezone.now,
    )

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        constraints = [
            UniqueConstraint(
                fields=('title', 'author', ),
                name='unique_title_author'
            )]
        ordering = ('-pub_date',)

    def __str__(self):
        return self.text[:40]


class Comment(Model):
    review = ForeignKey(
        Review,
        related_name='comments',
        on_delete=CASCADE,
        verbose_name='Отзыв на произведение',
    )
    text = TextField('Текст комментария',)
    author = ForeignKey(
        User,
        related_name='comments',
        on_delete=CASCADE,
        verbose_name='Автор комментария',
    )
    pub_date = DateTimeField(
        'Дата публикации комментария',
        default=timezone.now,
    )

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
        ordering = ('pub_date',)

    def __str__(self):
        return self.text[:40]
