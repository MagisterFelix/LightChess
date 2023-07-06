from django.core.exceptions import ValidationError
from django.db import models

from .base import BaseModel
from .user import User


class Game(BaseModel):

    class Time(models.IntegerChoices):
        MIN_3 = 0, "3 minutes"
        MIN_10 = 1, "10 minutes"
        MIN_30 = 2, "30 minutes"
        MIN_60 = 3, "60 minutes"

    class Result(models.IntegerChoices):
        PENDING = 0, "Pending"
        WIN_WHITE = 1, "White won"
        WIN_BLACK = 2, "Black won"
        DRAW = 3, "Draw"

    player_white = models.ForeignKey(User, on_delete=models.CASCADE, related_name="player_white")
    player_black = models.ForeignKey(User, on_delete=models.CASCADE, related_name="player_black")
    time_per_player = models.IntegerField(choices=Time.choices, default=Time.MIN_10)
    result = models.IntegerField(choices=Result.choices, default=Result.PENDING)
    created_at = models.DateTimeField(auto_now_add=True)

    def clean(self):
        super().clean()

        if self.player_white_id and self.player_black_id and self.player_white_id == self.player_black_id:
            raise ValidationError("Player cannot play against himself.", code="invalid")

    def __str__(self):
        return str(self.id)

    class Meta:
        db_table = "game"
