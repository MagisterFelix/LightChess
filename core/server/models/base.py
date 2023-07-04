from uuid import uuid4

from django.db import models


class BaseManager(models.Manager):

    def get_or_none(self, *args, **kwargs):
        try:
            return self.get(*args, **kwargs)
        except self.model.DoesNotExist:
            return None


class BaseModel(models.Model):

    id = models.UUIDField(
        primary_key=True,
        editable=False,
        unique=True,
        default=uuid4,
    )

    objects = BaseManager()

    class Meta:
        abstract = True
