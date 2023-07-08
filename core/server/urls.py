from django.urls import path

from core.server.views import AuthorizationView, DeauthorizationView, ProfileView, RegistrationView

urlpatterns = [
    path("sign-in/", AuthorizationView().as_view(), name="sign-in"),
    path("sign-up/", RegistrationView().as_view(), name="sign-up"),
    path("sign-out/", DeauthorizationView().as_view(), name="sign-out"),
    path("profile/", ProfileView().as_view(), name="profile"),
]
