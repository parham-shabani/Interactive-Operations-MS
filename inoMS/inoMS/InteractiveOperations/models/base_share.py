from django.db import models
from .base import InteractionBase

class AbstractShareBase(InteractionBase):

    actor_type = models.CharField(max_length=50)
    actor_id = models.CharField(max_length=100)
    target_type = models.CharField(max_length=50)
    target_id = models.CharField(max_length=100)
    platform = models.CharField(max_length=50)
    destination_type = models.CharField(max_length=50, null=True, blank=True)
    destination_id = models.CharField(max_length=100, null=True, blank=True)
    url = models.URLField(default='')     #tavasote app url page gharar migirad
    reason = models.TextField(null=True)
    created_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

