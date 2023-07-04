from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import models

from core.server.utils import ImageUtils

from .base import BaseManager, BaseModel


class UserManager(BaseUserManager, BaseManager):

    def create_user(self, username, password, **extra_fields):
        if username is None or username == "":
            raise ValueError("User must have an username.")

        if password is None or password == "":
            raise ValueError("User must have a password.")

        user = self.model(
            username=username,
            **extra_fields
        )
        user.set_password(password)
        user.save()

        return user

    def create_superuser(self, username, password, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        return self.create_user(username, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin, BaseModel):

    username_validator = UnicodeUsernameValidator()

    username = models.CharField(
        max_length=150,
        unique=True,
        validators=[username_validator],
        error_messages={
            "unique": "A user with that username already exists.",
        },
    )
    image = models.FileField(
        default=ImageUtils.get_default_avatar,
        upload_to=ImageUtils.upload_image_to,
        validators=[ImageUtils.validate_image_file_extension],
    )
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = "username"

    def delete(self, *args, **kwargs):
        ImageUtils.remove_image_from(self)
        super().delete(*args, **kwargs)

    def __str__(self):
        return self.username

    class Meta:
        db_table = "user"
