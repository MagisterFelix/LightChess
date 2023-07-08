import os

from django.conf import settings
from django.core.exceptions import ValidationError
from django.utils import timezone
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.backends import TokenBackend
from rest_framework_simplejwt.exceptions import TokenBackendError


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


class AuthorizationUtils:

    @staticmethod
    def _get_response(request, message, status):
        view = APIView()
        view.headers = view.default_response_headers

        data = {
            "details": message
        }

        response = Response(data=data, status=status)

        return view.finalize_response(request, response).render()

    @staticmethod
    def get_user_id(token):
        if token is None:
            return None

        try:
            user_id = TokenBackend(
                algorithm=settings.SIMPLE_JWT["ALGORITHM"],
                signing_key=settings.SIMPLE_JWT["SIGNING_KEY"]
            ).decode(token)["user_id"]
        except TokenBackendError:
            return None

        return user_id

    @staticmethod
    def set_auth_cookies(response, data):
        cookies = []

        if data.get("access") is not None:
            cookies.append({
                "key": settings.SIMPLE_JWT["AUTH_COOKIE_ACCESS_TOKEN"],
                "value": data["access"],
                "expires": timezone.now() + settings.SIMPLE_JWT["ACCESS_TOKEN_LIFETIME"],
                "httponly": settings.SIMPLE_JWT["AUTH_COOKIE_HTTP_ONLY"],
                "samesite": settings.SIMPLE_JWT['AUTH_COOKIE_SAMESITE'],
            })

        if data.get("refresh") is not None:
            cookies.append({
                "key": settings.SIMPLE_JWT["AUTH_COOKIE_REFRESH_TOKEN"],
                "value": data.get("refresh"),
                "expires": timezone.now() + settings.SIMPLE_JWT["REFRESH_TOKEN_LIFETIME"],
                "httponly": settings.SIMPLE_JWT["AUTH_COOKIE_HTTP_ONLY"],
                "samesite": settings.SIMPLE_JWT['AUTH_COOKIE_SAMESITE'],
            })

        for cookie in cookies:
            response.set_cookie(**cookie)

    @staticmethod
    def remove_auth_cookies(response):
        response.delete_cookie("access_token")
        response.delete_cookie("refresh_token")

    @staticmethod
    def get_invalid_csrftoken_response(request):
        message = "CSRF token is invalid or not provided."
        response = AuthorizationUtils._get_response(request, message, status.HTTP_403_FORBIDDEN)
        AuthorizationUtils.remove_auth_cookies(response)
        return response

    @staticmethod
    def get_missed_credentials_response(request):
        message = "Authentication credentials were not provided."
        response = AuthorizationUtils._get_response(request, message, status.HTTP_401_UNAUTHORIZED)
        return response

    @staticmethod
    def get_invalid_token_response(request):
        message = "Token is invalid or expired."
        response = AuthorizationUtils._get_response(request, message, status.HTTP_401_UNAUTHORIZED)
        AuthorizationUtils.remove_auth_cookies(response)
        return response
