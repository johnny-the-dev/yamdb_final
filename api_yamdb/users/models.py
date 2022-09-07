from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    ADMIN = 'admin'
    MODERATOR = 'moderator'
    USER = 'user'
    ROLES = (
        (ADMIN, 'admin'),
        (MODERATOR, 'moderator'),
        (USER, 'user'),
    )

    id = models.BigAutoField(primary_key=True)

    username = models.CharField(
        verbose_name='Никнейм',
        help_text='Имя пользователя',
        max_length=20,
        unique=True
    )
    email = models.EmailField(
        verbose_name='Email',
        help_text='Адрес электронной почты',
        unique=True
    )
    role = models.CharField(
        verbose_name='Статус пользователя',
        help_text='Права предоставляемые пользователю',
        max_length=20,
        choices=ROLES,
        default='user'
    )
    bio = models.TextField(
        verbose_name='Биография',
        help_text='Краткая биография пользователя',
        blank=True,
    )

    @property
    def is_moderator(self):
        return self.role == self.MODERATOR

    @property
    def is_admin(self):
        return self.role == self.ADMIN

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ('username', )

    class Meta:
        ordering = ('id', )
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.username
