import os

from django.conf import settings
from django.core.exceptions import ValidationError
from django.utils import timezone


class ImageUtils:

    @staticmethod
    def get_default_avatar():
        return "../static/avatar.svg"

    @staticmethod
    def validate_image_file_extension(file):
        valid_extensions = [".jpg", ".jpeg", ".png", ".svg"]
        extension = os.path.splitext(file.name)[1]

        if not extension.lower() in valid_extensions:
            raise ValidationError("The file uploaded either not an image or a corrupted image.")

    @staticmethod
    def upload_image_to(instance, filename):
        name = instance.username
        folder, title = "users", f"{name}-{int(timezone.now().timestamp())}"
        directory = os.path.join(settings.MEDIA_ROOT, f"{folder}")

        if not os.path.exists(directory):
            os.makedirs(directory)

        for file in os.listdir(directory):
            if file.startswith(f"{name}-"):
                os.remove(os.path.join(settings.MEDIA_ROOT, f"{folder}/{file}"))

        return f"{folder}/{title}{os.path.splitext(filename)[-1]}"

    @staticmethod
    def remove_image_from(instance):
        name = instance.image.name

        if "static" in name:
            return None

        path = instance.image.path

        if not os.path.exists(path):
            return None

        os.remove(path)
