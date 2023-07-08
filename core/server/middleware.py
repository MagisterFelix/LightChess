from django.contrib.auth import logout
from django.middleware.csrf import CsrfViewMiddleware
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.serializers import TokenRefreshSerializer, TokenVerifySerializer

from core.server.utils import AuthorizationUtils
from core.urls import urlpatterns

api = urlpatterns[1]

NON_REQUIRED_AUTHORIZATION = [
    "sign-in",
    "sign-up",
]
REQUIRED_AUTHORIZATION = [
    f"/{str(api.pattern) + url.name}/" for url in api.url_patterns if url.name not in NON_REQUIRED_AUTHORIZATION
]


class AuthorizationMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.path in (f"/api/{path}/" for path in NON_REQUIRED_AUTHORIZATION):
            request.COOKIES.get("sessionid") and logout(request)

        if all(request.path.find(path) == -1 for path in REQUIRED_AUTHORIZATION):
            return self.get_response(request)

        reason = CsrfViewMiddleware(self.get_response).process_view(request, None, (), {})
        if reason is not None:
            return AuthorizationUtils.get_invalid_csrftoken_response(request=reason)

        access = request.COOKIES.get("access_token")
        refresh = request.COOKIES.get("refresh_token")

        if not access:
            if not refresh:
                return AuthorizationUtils.get_missed_credentials_response(request=request)

            data = {
                "refresh": refresh
            }

            serializer = TokenRefreshSerializer(data=data)

            try:
                serializer.is_valid()
            except TokenError:
                return AuthorizationUtils.get_invalid_token_response(request=request)

            access = serializer.data["access"]

        data = {
            "token": access
        }

        try:
            TokenVerifySerializer(data=data).is_valid()
            request.META["HTTP_AUTHORIZATION"] = f"Bearer {access}"
        except TokenError:
            return AuthorizationUtils.get_invalid_token_response(request=request)

        response = self.get_response(request)

        if request.path != "/api/sign-out/":
            data = {
                "access": access,
                "refresh": refresh
            }
            AuthorizationUtils.set_auth_cookies(response, data)

        return response
