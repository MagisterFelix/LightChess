from django.db import models

from .base import BaseModel
from .game import Game


class Move(BaseModel):

    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    notation = models.CharField(max_length=8)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.id)

    class Meta:
        db_table = "move"
