from django.db import models
from .base import InteractionBase

class AbstractFollowBase(InteractionBase):
    actor_type = models.CharField(max_length=50)
    actor_id = models.CharField(max_length=100)
    target_type = models.CharField(max_length=50)
    target_id = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    last_updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
