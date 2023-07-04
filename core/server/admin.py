from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group
from django.utils.html import format_html

from .models import Game, Message, Move, User


@admin.register(User)
class UserAdmin(UserAdmin):

    def avatar(self, user):
        return format_html(f"<img src=\"{user.image.url}\" style=\"max-width: 128px; max-height: 128px\"/>")

    list_display = ("id", "username", "is_staff",)
    fieldsets = (
        (None, {
            "fields": (
                "username", "password",
            ),
        }),
        ("Personal info", {
            "fields": (
                "avatar", "image",
            ),
        }),
        ("Permissions", {
            "fields": (
                "is_staff", "is_superuser",
            ),
        }),
        ("Dates", {
            "fields": (
                "last_login",
            ),
        }),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": (
                    "wide",
                ),
                "fields": (
                    "username", "password1", "password2",
                ),
            }
        ),
    )
    readonly_fields = ("avatar", "last_login",)


@admin.register(Game)
class GameAdmin(admin.ModelAdmin):

    list_display = ("id", "result", "created_at",)
    fieldsets = (
        ("Information", {
            "fields": (
                "player_white", "player_black", "time_per_player", "result", "created_at",
            ),
        }),
    )
    readonly_fields = ("created_at",)


@admin.register(Move)
class MoveAdmin(admin.ModelAdmin):

    list_display = ("id", "game", "notation", "created_at",)
    fieldsets = (
        ("Information", {
            "fields": (
                "game", "notation", "created_at",
            ),
        }),
    )
    readonly_fields = ("created_at",)


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):

    list_display = ("id", "short_message", "game", "author", "created_at",)
    fieldsets = (
        ("Game", {
            "fields": (
                "game",
            ),
        }),
        ("Information", {
            "fields": (
                "author", "text", "created_at",
            ),
        }),
    )
    readonly_fields = ("created_at",)


admin.site.unregister(Group)
