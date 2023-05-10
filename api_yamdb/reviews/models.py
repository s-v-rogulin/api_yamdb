from django.core.validators import MaxValueValidator, MinValueValidator
from django.db.models import (
    CASCADE, SET_NULL, CharField, DateTimeField,
    ForeignKey, ManyToManyField, Model,
    PositiveIntegerField, SlugField, TextField,
    UniqueConstraint
)

from users.models import User


class Genre(Model):
    name = CharField(
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
        return self.name


class Category(Model):
    name = CharField(
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
        return self.name


class Title(Model):
    name = CharField(
        max_length=256,
    )
    description = TextField(
        null=True,
        blank=True,
    )
    year = PositiveIntegerField()
    genre = ManyToManyField(
        Genre,
        related_name='titles',
    )
    category = ForeignKey(
        Category,
        related_name='titles',
        on_delete=SET_NULL,
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'
        ordering = ('year',)

    def __str__(self):
        return self.name


class Review(Model):
    title = ForeignKey(
        Title,
        related_name='reviews',
        on_delete=CASCADE,
    )
    text = TextField()
    author = ForeignKey(
        User,
        related_name='reviews',
        on_delete=CASCADE,
    )
    score = PositiveIntegerField(
        validators=(
            MinValueValidator(1, 'Минимальная оценка - 1'),
            MaxValueValidator(10, 'Максимальная оценка - 10')
        ),
    )
    pub_date = DateTimeField(
        auto_now_add=True,
    )

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        constraints = [
            UniqueConstraint(
                fields=('title', 'author', ),
                name='unique_title_author'
            )]
        ordering = ('pub_date',)

    def __str__(self):
        return self.text


class Comment(Model):
    review = ForeignKey(
        Review,
        related_name='comments',
        on_delete=CASCADE
    )
    text = TextField()
    author = ForeignKey(
        User,
        related_name='comments',
        on_delete=CASCADE
    )
    pub_date = DateTimeField(
        auto_now_add=True,
    )

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
        ordering = ('pub_date',)

    def __str__(self):
        return self.text
