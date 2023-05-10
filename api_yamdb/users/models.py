from django.contrib.auth.models import AbstractUser
from django.db.models import (
    CharField,
    EmailField,
    TextChoices,
    TextField,
)


class User(AbstractUser):
    class Roles(TextChoices):
        USER = 'user', 'Пользователь'
        MODERATOR = 'moderator', 'Модератор'
        ADMINISTRATOR = 'admin', 'Администратор'
    username = CharField(
        max_length=150,
        unique=True,
    )
    email = EmailField(
        max_length=254,
        unique=True,
    )
    role = CharField(
        max_length=50,
        choices=Roles.choices,
        default=Roles.USER,
    )
    bio = TextField(
        blank=True,
        null=True,
    )
