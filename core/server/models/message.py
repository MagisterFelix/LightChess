from django.db import models
from django.template.defaultfilters import truncatechars

from .base import BaseModel
from .game import Game
from .user import User


class Message(BaseModel):

    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField(max_length=512)
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def short_message(self):
        return truncatechars(self.text, 32)

    def __str__(self):
        return self.short_message

    class Meta:
        db_table = "message"
