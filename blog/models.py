from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from datetime import date, timedelta

class CustomUserManager(BaseUserManager):
    def create_user(self, username, email, password=None, **extra_fields):
        if not email:
            raise ValueError(_('The Email field must be set'))
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('birth_date', date(1990, 1, 1))  # Явная дата

        return self.create_user(username, email, password, **extra_fields)

class CustomUser(AbstractUser):
    phone_number = models.CharField(_('phone number'), max_length=15, blank=True, null=True)
    birth_date = models.DateField(_('birth date'), blank=True, null=True)
    created_at = models.DateTimeField(_('created at'), auto_now_add=True)
    updated_at = models.DateTimeField(_('updated at'), auto_now=True)
    email = models.EmailField(
        _('email address'),
        unique=True,
    )

    groups = models.ManyToManyField(
        'auth.Group',
        related_name='custom_users',
        blank=True,
        verbose_name=_('groups')
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='custom_users',
        blank=True,
        verbose_name=_('user permissions')
    )

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'birth_date']

    def clean(self):
        if self.birth_date and isinstance(self.birth_date, date):
            if self.birth_date > timezone.now().date():
                raise ValidationError(_('Birth date cannot be in the future.'))
        else:
            raise ValidationError(_('Invalid birth date format'))

class Post(models.Model):
    title = models.CharField(_('title'), max_length=255)
    text = models.TextField(_('text'))
    image = models.ImageField(_('image'), upload_to='posts/', blank=True, null=True)
    author = models.ForeignKey(
        'CustomUser',
        on_delete=models.CASCADE,
        related_name='posts',
        verbose_name=_('author')
    )
    created_at = models.DateTimeField(_('created at'), auto_now_add=True)
    updated_at = models.DateTimeField(_('updated at'), auto_now=True)

    forbidden_words = ['ерунда', 'глупость', 'чепуха']

    def __str__(self):
        return self.title

    def clean(self):
        if self.author.birth_date:
            today = timezone.now().date()
            age = today.year - self.author.birth_date.year - (
                (today.month, today.day) < (self.author.birth_date.month, self.author.birth_date.day)
            )
            if age < 18:
                raise ValidationError(_('Author must be at least 18 years old.'))

        if any(word in self.title.lower() for word in self.forbidden_words):
            raise ValidationError(_('Title contains forbidden words.'))

        super().clean()

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

class Comment(models.Model):
    author = models.ForeignKey(
        'CustomUser',
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name=_('author')
    )
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name=_('post')
    )
    text = models.TextField(_('text'))
    created_at = models.DateTimeField(_('created at'), auto_now_add=True)
    updated_at = models.DateTimeField(_('updated at'), auto_now=True)

    def __str__(self):
        return f'{self.author.username} on {self.post.title}'