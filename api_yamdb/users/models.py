from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db.models import CharField, EmailField, TextChoices, TextField


class User(AbstractUser):
    class Roles(TextChoices):
        USER = 'user', 'Пользователь'
        MODERATOR = 'moderator', 'Модератор'
        ADMIN = 'admin', 'Администратор'
    username = CharField(
        max_length=150,
        unique=True,
        validators=(UnicodeUsernameValidator(),)
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

    is_admin = property(
        lambda self: self.is_superuser or self.role == self.Roles.ADMIN
    )
    is_moderator = property(
        lambda self: self.role == self.Roles.MODERATOR
    )
